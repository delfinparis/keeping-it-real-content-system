#!/usr/bin/env python3
"""
Polish v2 scripts to v3 format.

Adds:
- Brand intro: "This is D.J. Paris with Keeping It Real Podcast,
  and this is your agent tip of the day."
- Close: "See you next time."
- All v2.0 engagement principles (curiosity gap, mirror moment,
  15-sec re-hook, contrast structure, ON-SCREEN callouts, etc.)

Usage:
  python scripts/polish_scripts.py                    # Polish all unprocessed v2 scripts
  python scripts/polish_scripts.py --limit 10         # Polish next 10 only
  python scripts/polish_scripts.py --file FILENAME    # Polish one specific file
  python scripts/polish_scripts.py --dry-run          # Preview what would run
  python scripts/polish_scripts.py --provider openai  # Use OpenAI instead
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Load .env file if present (ANTHROPIC_API_KEY or OPENAI_API_KEY)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass  # dotenv optional; set env vars manually if needed

# Reuse API wrappers from analyze_episodes
import sys
sys.path.insert(0, str(Path(__file__).parent))
from analyze_episodes import (
    analyze_with_anthropic,
    analyze_with_openai,
    ANTHROPIC_AVAILABLE,
    OPENAI_AVAILABLE,
)

PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "content" / "scripts"

POLISH_PROMPT = """You are an expert short-form video script writer for D.J. Paris, VP of Business Development at Kale Realty and host of Keeping It Real Podcast (700+ episodes, 3.2M+ downloads).

Take this existing video script draft and rewrite it into a polished, camera-ready version.

ORIGINAL SCRIPT:
{existing_script}

GUEST: {guest_name}
CLIP TYPE: {clip_type}

---

MANDATORY STRUCTURE (in this exact order — do not reorder):

**HOOK (0:00–0:08)**
The FIRST words out of D.J.'s mouth. No name, no setup. A pattern interrupt — surprising statement, bold claim, or question that stops the scroll. Under 15 words. Opens a curiosity gap the rest of the video must close.

**BRAND INTRO (0:08–0:12)**
Exactly this line, said quickly and naturally: "This is D.J. Paris with Keeping It Real Podcast, and this is your agent tip of the day."

**SETUP (0:12–0:22)**
Context — who said this, where it came from, why it matters. Create a "mirror moment": describe the viewer's specific situation so precisely they think "that's me." Name the pain. Do NOT give the solution yet.
End with a 15-second re-hook line: something like "But here's the part nobody talks about..." or "And this is where most agents get it completely wrong."

**INSIGHT (0:22–0:45)**
The actual advice, tactic, or story from the guest. Be specific and tactical. Use the guest's real words where possible. Add [ON-SCREEN: key phrase or stat] markers at every key beat for muted viewers. If there's a contrast, use it: "Most agents do X. Top producers do Y."

**REFRAME/APPLICATION (0:45–0:55)**
Why this matters right now. How to apply it this week. "You can do this today." Include a credibility signal where natural.

**CTA (0:55–1:00+)**
One specific question that invites a comment. Make it easy and direct. Example: "Are you doing this already — yes or no?"

**CLOSE**
Exactly this line: "See you next time."

---

ENGAGEMENT PRINCIPLES — apply all of these:
1. CURIOSITY GAP — Hook opens a loop; don't close it until INSIGHT.
2. MIRROR MOMENT — Recreate the viewer's exact frustration in SETUP.
3. CONTRAST STRUCTURE — "Most agents do X. Top producers do Y." where natural.
4. HYPER-SPECIFIC NUMBERS — Specific numbers beat vague claims every time.
5. ON-SCREEN TEXT — Add [ON-SCREEN: ...] markers at every key beat (80% watch muted).
6. SHAREABLE MOMENT — One sentence so quotable a viewer would screenshot it.
7. EMOTIONAL ARC — Curious → Seen → Enlightened → Motivated → Engaged → Satisfied.
8. PACING — HOOK is punchy (under 12 words). BRAND INTRO said fast. INSIGHT can breathe.

---

Output format:

HOOK: [text] [ON-SCREEN: ...]
BRAND INTRO: "This is D.J. Paris with Keeping It Real Podcast, and this is your agent tip of the day."
SETUP: [text] [ON-SCREEN: ...]
  [15-SEC RE-HOOK]: [line]
INSIGHT: [text] [ON-SCREEN: ...]
REFRAME: [text]
CTA: "[question]"
CLOSE: "See you next time."

---

CAPTION: [under 150 characters]
HASHTAGS: [5 hashtags]
SHAREABLE_MOMENT: "[the one sentence most likely to be screenshotted]"
PERFORMANCE_NOTES: [3 delivery notes for D.J. on pacing, emphasis, eye contact]"""


def build_existing_script_text(script_data: dict) -> tuple[str, str, str]:
    """Extract readable script text, guest name, and clip type from a v2 JSON file."""
    metadata = script_data.get("_metadata", {})
    clip_assessment = script_data.get("clip_assessment", {})
    script = script_data.get("script", {})

    guest_name = metadata.get("guest_name", "Unknown Guest")
    clip_type = clip_assessment.get("clip_type", "tactical_specificity")

    parts = []

    # Include the original clip quote for context
    verbatim = clip_assessment.get("verbatim_quote", "")
    if verbatim:
        parts.append(f'ORIGINAL QUOTE: "{verbatim}"')
        parts.append("")

    for beat in ["HOOK", "SETUP", "INSIGHT", "REFRAME", "CTA"]:
        if beat in script:
            text = script[beat].get("text", "")
            if text:
                parts.append(f"{beat}: {text}")

    return "\n".join(parts), guest_name, clip_type


def polish_one(script_path: Path, provider: str = "anthropic") -> str:
    """Polish a single v2 script file and return the polished text."""
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)

    existing_text, guest_name, clip_type = build_existing_script_text(script_data)

    prompt = POLISH_PROMPT.format(
        existing_script=existing_text,
        guest_name=guest_name,
        clip_type=clip_type,
    )

    if provider == "openai":
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed.")
        return analyze_with_openai(prompt)
    else:
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package not installed.")
        return analyze_with_anthropic(prompt)


def save_v3(script_path: Path, polished_text: str, original_data: dict):
    """Save polished script as a v3 JSON file next to the v2 original."""
    v3_path = Path(str(script_path).replace("_v2.json", "_v3.json"))

    v3_data = {
        "polished_script": polished_text,
        "_metadata": {
            **original_data.get("_metadata", {}),
            "polished_at": datetime.now().isoformat(),
            "polish_version": "v3",
            "source_version": "v2",
            "source_file": script_path.name,
        },
    }

    with open(v3_path, "w", encoding="utf-8") as f:
        json.dump(v3_data, f, indent=2, ensure_ascii=False)

    return v3_path


def get_pending_files(specific_file: str = None) -> list[Path]:
    """Return v2 script files that don't yet have a v3 version."""
    if specific_file:
        path = SCRIPTS_DIR / specific_file
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return [path]

    v2_files = sorted(SCRIPTS_DIR.glob("*_v2.json"))
    pending = []
    for f in v2_files:
        v3 = Path(str(f).replace("_v2.json", "_v3.json"))
        if not v3.exists():
            pending.append(f)
    return pending


def main():
    parser = argparse.ArgumentParser(
        description="Polish v2 scripts to v3 with brand intro, close, and engagement principles"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        default="anthropic",
        help="AI provider to use (default: anthropic)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max number of scripts to polish in this run (0 = all)",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Polish a specific file by name (e.g. 2026-01-30_item1_Amanda-Pendleton_clip0_v2.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without calling the API",
    )
    args = parser.parse_args()

    try:
        pending = get_pending_files(args.file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    if args.limit > 0:
        pending = pending[: args.limit]

    print(f"\nScripts to polish: {len(pending)}")
    if not pending:
        print("Nothing to do — all v2 scripts already have v3 versions.")
        return

    if args.dry_run:
        for f in pending:
            print(f"  {f.name}")
        return

    success = 0
    errors = 0

    for i, script_path in enumerate(pending, 1):
        print(f"\n[{i}/{len(pending)}] {script_path.name}")
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                original_data = json.load(f)

            polished_text = polish_one(script_path, provider=args.provider)
            v3_path = save_v3(script_path, polished_text, original_data)
            print(f"  Saved → {v3_path.name}")
            success += 1
        except Exception as e:
            print(f"  Error: {e}")
            errors += 1
            continue

    print(f"\n{'='*50}")
    print(f"Done. Polished: {success}  Errors: {errors}")
    print(f"v3 files saved to: {SCRIPTS_DIR}")


if __name__ == "__main__":
    main()
