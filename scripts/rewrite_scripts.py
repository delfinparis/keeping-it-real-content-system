#!/usr/bin/env python3
"""
Script Rewriter — Takes REWRITE-verdict scripts from Kill Judge,
feeds them back through with the judge's specific feedback,
and generates improved versions with stronger CTAs.
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

SYSTEM_PROMPT = """You are a script rewriter. You receive a 60-second video script that was scored by a quality judge and found to need improvement. You also receive the judge's specific feedback.

Your job: Rewrite the script to fix the identified problems while keeping what works.

Your PRIMARY focus this round: CTAs (Calls to Action). The #1 recurring weakness is vague, reflective CTAs like "ask yourself..." or "think about..." Instead, every CTA must give a SPECIFIC, CONCRETE action the viewer can take in the next 60 seconds or 24 hours.

CTA RULES:
1. Name the EXACT action: "Open your CRM right now. Filter by 'last contacted 90+ days ago.' Call the first three." NOT "Start reconnecting with your database."
2. Make it so specific they can picture doing it: "Tomorrow morning before your first showing, record a 30-second video walking through ONE thing buyers miss in that neighborhood." NOT "Start making video content."
3. Create urgency without being cheesy: "Your next listing appointment is probably this week. Before you walk in, ask yourself one question..." NOT "Ready to transform your business?"
4. If the insight is mindset-based (not tactical), the CTA should bridge to action: "Tonight, write down the one client conversation you've been avoiding. Tomorrow at 9am, make that call. That's the pattern breaking." NOT "Reflect on your patterns."

ADDITIONAL FIXES:
- If the judge flagged the HOOK, sharpen it — more specific, more provocative, less generic.
- If the judge flagged SPECIFICITY, add concrete numbers, names, tools, or steps.
- If the judge flagged VOICE, make it sound more like speech and less like copywriting.
- Keep production notes. Improve them if you can.
- Keep what the judge praised (strongest_line). Build around it.

Return ONLY valid JSON. No markdown code blocks."""


def build_rewrite_prompt(script_data, judge_review):
    """Build the rewrite prompt with original script + judge feedback."""

    # Extract script sections
    script = script_data.get("script", {})
    sections = ""
    for key in ["HOOK", "SETUP", "INSIGHT", "REFRAME", "CTA"]:
        if key in script:
            section = script[key]
            if isinstance(section, dict):
                text = section.get("text", "")
                prod = section.get("production_note", "")
                sections += f"\n{key}: {text}"
                if prod:
                    sections += f"\n  [Production: {prod}]"
            else:
                sections += f"\n{key}: {section}"

    clip = script_data.get("clip_assessment", {})
    meta = script_data.get("_metadata", {})

    return f"""ORIGINAL SCRIPT TO REWRITE:

Guest: {meta.get('guest_name', 'Unknown')}
Target Avatar: {script_data.get('target_avatar', clip.get('target_avatar', 'unknown'))}
Content Pillar: {script_data.get('content_pillar', 'unknown')}
Original Quote: "{clip.get('verbatim_quote', '')}"
Guest Voice: {clip.get('guest_voice', 'Unknown style')}
Energy: {clip.get('energy', 'Unknown')}

{sections}

CAPTION: {script_data.get('caption', '')}

---

KILL JUDGE FEEDBACK:
- Score: {judge_review.get('score', '?')}/10
- Verdict: {judge_review.get('verdict', '?')}
- Hook Power: {judge_review.get('hook_power', '?')}/10
- Specificity: {judge_review.get('specificity', '?')}/10
- Voice Authenticity: {judge_review.get('voice_authenticity', '?')}/10
- Viewer Action: {judge_review.get('viewer_action', '?')}/10
- Emotional Pull: {judge_review.get('emotional_pull', '?')}/10
- Strongest Line: "{judge_review.get('strongest_line', 'N/A')}"
- Weakest Line: "{judge_review.get('weakest_line', 'N/A')}"
- Specific Fix Needed: {judge_review.get('one_line_note', 'N/A')}

---

Rewrite this script. Keep the strongest line. Fix the weakest line. Make the CTA brutally specific and actionable.

Return as JSON:

{{
  "script": {{
    "HOOK": {{
      "timing": "0:00-0:03",
      "text": "<Improved hook — keep if judge scored 7+, sharpen if below>",
      "production_note": "<Visual direction>"
    }},
    "SETUP": {{
      "timing": "0:03-0:12",
      "text": "<Improved setup>",
      "production_note": "<Visual direction>"
    }},
    "INSIGHT": {{
      "timing": "0:12-0:38",
      "text": "<Improved insight — more specific, more concrete, more the guest's voice>",
      "production_note": "<Visual direction>"
    }},
    "REFRAME": {{
      "timing": "0:38-0:50",
      "text": "<Improved reframe — paint the specific picture for this avatar>",
      "production_note": "<Visual direction>"
    }},
    "CTA": {{
      "timing": "0:50-0:60",
      "text": "<COMPLETELY REWRITTEN CTA — must name a specific action with a specific timeframe. No 'ask yourself.' No 'think about.' Name the verb, the object, and the deadline.>",
      "production_note": "<Visual direction — text overlay of the action step>"
    }}
  }},
  "caption": "<Improved caption — under 150 chars, conversational>",
  "hashtags": {json.dumps(script_data.get('hashtags', []))},
  "content_pillar": "{script_data.get('content_pillar', 'unknown')}",
  "target_avatar": "{script_data.get('target_avatar', clip.get('target_avatar', 'unknown'))}",
  "share_trigger": "<identity | utility | debate>",
  "rewrite_changelog": "<1-2 sentences: what you changed and why>"
}}"""


def rewrite_script(client, script_data, judge_review, model="claude-sonnet-4-5-20250929"):
    """Rewrite a single script using the judge's feedback."""
    prompt = build_rewrite_prompt(script_data, judge_review)

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM_PROMPT,
        temperature=0.7,
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = re.sub(r'^```json?\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)

    try:
        rewritten = json.loads(raw)
    except json.JSONDecodeError:
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            try:
                rewritten = json.loads(json_match.group())
            except json.JSONDecodeError:
                rewritten = {"raw_response": raw, "parse_error": True}
        else:
            rewritten = {"raw_response": raw, "parse_error": True}

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return rewritten, usage


def main():
    parser = argparse.ArgumentParser(description="Rewrite scripts flagged by Kill Judge")
    parser.add_argument("--report", type=str, help="Path to kill judge report JSON")
    parser.add_argument("--model", type=str, default="claude-sonnet-4-5-20250929")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()

    # Find the most recent report
    if args.report:
        report_path = Path(args.report)
    else:
        reports = sorted(REPORTS_DIR.glob("kill_judge_report_*.json"), reverse=True)
        if not reports:
            print("No kill judge reports found. Run kill_judge.py first.")
            return
        report_path = reports[0]

    print(f"Using report: {report_path.name}")

    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    # Get REWRITE verdicts
    rewrites = [r for r in report["reviews"] if r.get("verdict") == "REWRITE"]
    print(f"Scripts to rewrite: {len(rewrites)}")

    if args.dry_run:
        print("\n[DRY RUN] Would rewrite:")
        for r in rewrites[:10]:
            print(f"  {r['score']}/10 — {r['script_id'][:50]}")
            print(f"    Fix: {r.get('one_line_note', 'N/A')[:80]}")
        if len(rewrites) > 10:
            print(f"  ... and {len(rewrites) - 10} more")
        est_cost = len(rewrites) * (2500 * 3 + 1500 * 15) / 1_000_000
        print(f"\nEstimated cost: ~${est_cost:.2f}")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic()

    total_input = 0
    total_output = 0
    rewritten_count = 0
    errors = 0
    start_time = time.time()

    for i, review in enumerate(rewrites):
        script_id = review.get("script_id", "")
        script_path = SCRIPTS_DIR / script_id

        if not script_path.exists():
            print(f"  [{i+1}/{len(rewrites)}] SKIP (not found): {script_id}")
            errors += 1
            continue

        with open(script_path, "r", encoding="utf-8") as f:
            original = json.load(f)

        guest = original.get("_metadata", {}).get("guest_name", "Unknown")
        print(f"  [{i+1}/{len(rewrites)}] {guest} — {script_id[:45]}...", end="", flush=True)

        try:
            rewritten, usage = rewrite_script(client, original, review, args.model)
            total_input += usage["input_tokens"]
            total_output += usage["output_tokens"]

            if "parse_error" not in rewritten:
                # Preserve original metadata + clip_assessment, update script
                original["script"] = rewritten.get("script", original.get("script"))
                original["caption"] = rewritten.get("caption", original.get("caption"))
                original["share_trigger"] = rewritten.get("share_trigger", original.get("share_trigger"))

                # Add rewrite metadata
                original["_metadata"]["rewritten_at"] = datetime.now().isoformat()
                original["_metadata"]["rewrite_version"] = "v2.1"
                original["_metadata"]["rewrite_changelog"] = rewritten.get("rewrite_changelog", "")
                original["_metadata"]["original_score"] = review.get("score")
                original["_metadata"]["judge_note"] = review.get("one_line_note", "")

                with open(script_path, "w", encoding="utf-8") as f:
                    json.dump(original, f, indent=2, ensure_ascii=False)

                rewritten_count += 1
                changelog = rewritten.get("rewrite_changelog", "")[:60]
                print(f" ✓ ({changelog})")
            else:
                print(f" ✗ (parse error)")
                errors += 1

        except Exception as e:
            print(f" ✗ ({e})")
            errors += 1

        if i < len(rewrites) - 1:
            time.sleep(args.delay)

        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed * 60
            remaining = (len(rewrites) - i - 1) / rate if rate > 0 else 0
            print(f"\n  --- Progress: {rewritten_count}/{len(rewrites)}, "
                  f"{errors} errors, ~{remaining:.0f}min remaining ---\n")

    elapsed = time.time() - start_time
    est_cost = (total_input * 3 / 1_000_000) + (total_output * 15 / 1_000_000)

    print(f"\n{'='*60}")
    print(f"REWRITE COMPLETE")
    print(f"{'='*60}")
    print(f"Scripts rewritten: {rewritten_count}")
    print(f"Errors: {errors}")
    print(f"Tokens: {total_input:,} input + {total_output:,} output")
    print(f"Cost: ${est_cost:.2f}")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"\nAll rewrites saved in-place (originals overwritten).")
    print(f"Rewrite metadata added to _metadata.rewrite_version = 'v2.1'")


if __name__ == "__main__":
    main()
