#!/usr/bin/env python3
"""
Kill Judge — Quality gate for V2 video scripts.
Scores each script 1-10 and assigns a verdict: PUBLISH, REWRITE, or KILL.
Processes scripts in batches of 5 to reduce API calls.
"""

import os
import json
import sys
import time
import argparse
import re
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "content" / "scripts"
REPORTS_DIR = PROJECT_ROOT / "content" / "kill_judge_reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """You are the kill judge. Your job is to score short-form video scripts on a 1-10 scale and decide: PUBLISH, REWRITE, or KILL.

You have seen what works and what doesn't on TikTok, Instagram Reels, and YouTube Shorts. You know the difference between a script a team is proud of internally and one that actually stops thumbs in the wild.

Your biases (and they are correct):

1. HOOKS: If the first sentence doesn't make you want to hear the second sentence, the score caps at 4. Nothing else matters if the hook fails.

2. SPECIFICITY: Vague advice gets a vague response (scroll past). Specific tactics get saves and shares. "Prospect more" = 2. "Call 10 FSBOs every Tuesday at 9am using this exact script" = 8.

3. VOICE: If the script sounds like it was written by a marketing department, subtract 2 points. If it sounds like a real person talking to a friend, add 1.

4. THE "SO WHAT" TEST: After reading the script, can you complete this sentence: "After watching this, the viewer will ___." If the blank is "feel inspired" — that's a 5. If the blank is "open YouTube and search their zip code" — that's an 8.

5. PRODUCTION FEASIBILITY: A brilliant script that can't be filmed effectively is worth nothing. No production notes = subtract 1.

6. GUEST AUTHENTICITY: Does this sound like the guest, or like a copywriter? If you could swap the guest name for anyone else and the script still works — it's too generic. Subtract 2.

SCORING GUIDE:
- 9-10: Publish immediately. This will perform. Rare — maybe 1 in 20 scripts.
- 7-8: Publish with minor tweaks. Strong core, needs polish.
- 5-6: Rewrite. The source material is good but the script doesn't do it justice.
- 3-4: Rewrite from scratch. Wrong angle, wrong hook, or wrong avatar targeting.
- 1-2: Kill. The source clip isn't strong enough or the topic is too generic to stand out.

VERDICT RULES:
- PUBLISH: Score 7+
- REWRITE: Score 4-6
- KILL: Score 1-3

Be honest. A batch where every script scores 8+ is a lie. A batch with real variance is the truth.

Return ONLY valid JSON. No markdown code blocks. No additional text."""


def build_judge_prompt(scripts_batch):
    """Build the judge prompt for a batch of scripts."""
    scripts_text = ""
    for i, (filename, script) in enumerate(scripts_batch):
        # Extract the key parts for judging
        hook_text = ""
        setup_text = ""
        insight_text = ""
        reframe_text = ""
        cta_text = ""
        has_production_notes = False

        if "script" in script:
            s = script["script"]
            for key in ["HOOK", "SETUP", "INSIGHT", "REFRAME", "CTA"]:
                if key in s:
                    section = s[key]
                    if isinstance(section, dict):
                        text = section.get("text", "")
                        if section.get("production_note"):
                            has_production_notes = True
                    else:
                        text = str(section)

                    if key == "HOOK": hook_text = text
                    elif key == "SETUP": setup_text = text
                    elif key == "INSIGHT": insight_text = text
                    elif key == "REFRAME": reframe_text = text
                    elif key == "CTA": cta_text = text

        guest = script.get("_metadata", {}).get("guest_name", "Unknown")
        avatar = script.get("target_avatar", script.get("clip_assessment", {}).get("target_avatar", "unknown"))
        pillar = script.get("content_pillar", "unknown")
        quote = script.get("clip_assessment", {}).get("verbatim_quote", "")
        caption = script.get("caption", "")

        scripts_text += f"""
--- SCRIPT {i+1}: {filename} ---
Guest: {guest}
Target Avatar: {avatar}
Content Pillar: {pillar}
Original Quote: "{quote}"
Has Production Notes: {has_production_notes}

HOOK: {hook_text}
SETUP: {setup_text}
INSIGHT: {insight_text}
REFRAME: {reframe_text}
CTA: {cta_text}
CAPTION: {caption}
"""

    return f"""Review these {len(scripts_batch)} scripts and score each one.

{scripts_text}

---

Return a JSON object with this structure:

{{
  "reviews": [
    {{
      "script_id": "<filename>",
      "verdict": "<PUBLISH | REWRITE | KILL>",
      "score": <1-10>,
      "hook_power": <1-10>,
      "specificity": <1-10>,
      "voice_authenticity": <1-10>,
      "viewer_action": <1-10>,
      "emotional_pull": <1-10>,
      "strongest_line": "<Quote the single best line>",
      "weakest_line": "<Quote the single worst line>",
      "one_line_note": "<One sentence: what would make this script better? Be specific.>"
    }}
  ],
  "batch_top_pick": "<filename of the best script in this batch>",
  "batch_pattern": "<Any recurring issue across these scripts? One sentence.>"
}}"""


def judge_batch(client, scripts_batch, model="claude-sonnet-4-5-20250929"):
    """Send a batch to the kill judge and return scores."""
    prompt = build_judge_prompt(scripts_batch)

    response = client.messages.create(
        model=model,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM_PROMPT,
        temperature=0.3,
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = re.sub(r'^```json?\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            try:
                result = json.loads(json_match.group())
            except json.JSONDecodeError:
                result = {"raw_response": raw, "parse_error": True}
        else:
            result = {"raw_response": raw, "parse_error": True}

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return result, usage


def main():
    parser = argparse.ArgumentParser(description="Run Kill Judge quality gate on V2 scripts")
    parser.add_argument("--batch-size", type=int, default=5, help="Scripts per API call (default: 5)")
    parser.add_argument("--model", type=str, default="claude-sonnet-4-5-20250929")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=float, default=1.5)
    args = parser.parse_args()

    # Load all V2 scripts
    script_files = sorted(SCRIPTS_DIR.glob("*_v2.json"))
    if not script_files:
        print("No V2 scripts found in content/scripts/")
        return

    scripts = []
    for sf in script_files:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "parse_error" not in data:
            scripts.append((sf.name, data))

    print(f"\n{'='*60}")
    print(f"Kill Judge — Quality Gate")
    print(f"{'='*60}")
    print(f"Scripts to review: {len(scripts)}")
    print(f"Batch size: {args.batch_size}")
    print(f"API calls needed: {(len(scripts) + args.batch_size - 1) // args.batch_size}")
    print()

    if args.dry_run:
        print("[DRY RUN] Would review:")
        for name, _ in scripts[:10]:
            print(f"  - {name}")
        if len(scripts) > 10:
            print(f"  ... and {len(scripts) - 10} more")
        est_calls = (len(scripts) + args.batch_size - 1) // args.batch_size
        est_cost = est_calls * (4000 * 3 + 2000 * 15) / 1_000_000
        print(f"\nEstimated cost: ~${est_cost:.2f}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic()

    # Process in batches
    all_reviews = []
    total_input = 0
    total_output = 0
    batch_num = 0
    start_time = time.time()

    for i in range(0, len(scripts), args.batch_size):
        batch = scripts[i:i + args.batch_size]
        batch_num += 1
        total_batches = (len(scripts) + args.batch_size - 1) // args.batch_size
        names = [n for n, _ in batch]

        print(f"  [Batch {batch_num}/{total_batches}] Reviewing {len(batch)} scripts...", end="", flush=True)

        try:
            result, usage = judge_batch(client, batch, args.model)
            total_input += usage["input_tokens"]
            total_output += usage["output_tokens"]

            if "reviews" in result:
                for review in result["reviews"]:
                    all_reviews.append(review)
                    verdict = review.get("verdict", "?")
                    score = review.get("score", "?")
                    sid = review.get("script_id", "?")[:40]
                    symbol = "✓" if verdict == "PUBLISH" else ("↻" if verdict == "REWRITE" else "✗")
                    print(f"\n    {symbol} {sid}... → {verdict} ({score}/10)", end="")

                if "batch_top_pick" in result:
                    print(f"\n    ★ Top pick: {result['batch_top_pick']}", end="")
                if "batch_pattern" in result:
                    print(f"\n    Note: {result['batch_pattern']}", end="")

            print()

        except Exception as e:
            print(f" ERROR: {e}")

        if i + args.batch_size < len(scripts):
            time.sleep(args.delay)

    # Compile results
    publish = [r for r in all_reviews if r.get("verdict") == "PUBLISH"]
    rewrite = [r for r in all_reviews if r.get("verdict") == "REWRITE"]
    kill = [r for r in all_reviews if r.get("verdict") == "KILL"]

    scores = [r.get("score", 0) for r in all_reviews if isinstance(r.get("score"), (int, float))]
    avg_score = sum(scores) / len(scores) if scores else 0

    elapsed = time.time() - start_time
    est_cost = (total_input * 3 / 1_000_000) + (total_output * 15 / 1_000_000)

    # Save report
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_reviewed": len(all_reviews),
        "summary": {
            "publish": len(publish),
            "rewrite": len(rewrite),
            "kill": len(kill),
            "average_score": round(avg_score, 1),
            "score_distribution": {
                "9-10": len([s for s in scores if s >= 9]),
                "7-8": len([s for s in scores if 7 <= s < 9]),
                "5-6": len([s for s in scores if 5 <= s < 7]),
                "3-4": len([s for s in scores if 3 <= s < 5]),
                "1-2": len([s for s in scores if s < 3]),
            },
        },
        "reviews": sorted(all_reviews, key=lambda x: x.get("score", 0), reverse=True),
        "top_10": sorted(all_reviews, key=lambda x: x.get("score", 0), reverse=True)[:10],
        "needs_rewrite": [r for r in all_reviews if r.get("verdict") == "REWRITE"],
        "killed": [r for r in all_reviews if r.get("verdict") == "KILL"],
        "cost": {
            "input_tokens": total_input,
            "output_tokens": total_output,
            "estimated_cost_usd": round(est_cost, 2),
        },
    }

    report_path = REPORTS_DIR / f"kill_judge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print(f"KILL JUDGE REPORT")
    print(f"{'='*60}")
    print(f"Scripts reviewed: {len(all_reviews)}")
    print(f"Average score: {avg_score:.1f}/10")
    print()
    print(f"  PUBLISH (7+):  {len(publish)} scripts")
    print(f"  REWRITE (4-6): {len(rewrite)} scripts")
    print(f"  KILL (1-3):    {len(kill)} scripts")
    print()
    print(f"Score distribution:")
    print(f"  9-10: {report['summary']['score_distribution']['9-10']}")
    print(f"  7-8:  {report['summary']['score_distribution']['7-8']}")
    print(f"  5-6:  {report['summary']['score_distribution']['5-6']}")
    print(f"  3-4:  {report['summary']['score_distribution']['3-4']}")
    print(f"  1-2:  {report['summary']['score_distribution']['1-2']}")
    print()

    if publish:
        print("TOP 5 SCRIPTS:")
        for r in sorted(publish, key=lambda x: x.get("score", 0), reverse=True)[:5]:
            print(f"  ★ {r.get('score')}/10 — {r.get('script_id', '?')[:50]}")
            print(f"    Best line: \"{r.get('strongest_line', 'N/A')[:80]}\"")
        print()

    if kill:
        print("KILLED SCRIPTS:")
        for r in kill:
            print(f"  ✗ {r.get('score')}/10 — {r.get('script_id', '?')[:50]}")
            print(f"    Reason: {r.get('one_line_note', 'N/A')[:80]}")
        print()

    print(f"Tokens: {total_input:,} input + {total_output:,} output")
    print(f"Cost: ${est_cost:.2f}")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
