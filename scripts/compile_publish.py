#!/usr/bin/env python3
"""
compile_publish.py
------------------
Reads the kill judge report, collects all PUBLISH-verdict scripts,
loads each script file, and compiles them into a single organized
JSON file sorted by score (desc) then guest name (alpha).
"""

import json
import os
from datetime import datetime, timezone

REPORT_PATH = "/Users/djparis/unstuckagent-review/content/kill_judge_reports/kill_judge_report_20260219_113425.json"
SCRIPTS_DIR = "/Users/djparis/unstuckagent-review/content/scripts"
OUTPUT_PATH = "/Users/djparis/unstuckagent-review/content/publish_ready.json"


def main():
    with open(REPORT_PATH, "r") as f:
        report = json.load(f)

    publish_reviews = [r for r in report["reviews"] if r["verdict"] == "PUBLISH"]
    print(f"Found {len(publish_reviews)} PUBLISH verdicts in kill judge report.")

    compiled_scripts = []
    missing = []

    for review in publish_reviews:
        script_id = review["script_id"]
        script_path = os.path.join(SCRIPTS_DIR, script_id)

        if not os.path.exists(script_path):
            missing.append(script_id)
            print(f"  WARNING: Script file not found: {script_id}")
            continue

        with open(script_path, "r") as f:
            script_data = json.load(f)

        guest_name = script_data.get("_metadata", {}).get("guest_name", "Unknown")

        entry = {
            "score": review["score"],
            "judge_note": review.get("one_line_note", ""),
            "strongest_line": review.get("strongest_line", ""),
            "filename": script_id,
            "guest_name": guest_name,
            "target_avatar": script_data.get("target_avatar", ""),
            "content_pillar": script_data.get("content_pillar", ""),
            "clip_assessment": script_data.get("clip_assessment", {}),
            "script": script_data.get("script", {}),
            "caption": script_data.get("caption", ""),
            "hashtags": script_data.get("hashtags", []),
            "share_trigger": script_data.get("share_trigger", ""),
        }

        compiled_scripts.append(entry)

    compiled_scripts.sort(key=lambda x: (-x["score"], x["guest_name"].lower()))

    score_summary = {}
    for entry in compiled_scripts:
        s = str(entry["score"])
        score_summary[s] = score_summary.get(s, 0) + 1

    score_summary = {k: score_summary[k] for k in sorted(score_summary.keys(), key=lambda x: -int(x))}

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_scripts": len(compiled_scripts),
        "score_summary": score_summary,
        "scripts": compiled_scripts,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 50)
    print("  PUBLISH-READY COMPILATION COMPLETE")
    print("=" * 50)
    print(f"  Output: {OUTPUT_PATH}")
    print(f"  Total scripts compiled: {len(compiled_scripts)}")
    print()
    print("  Score Tier Breakdown:")
    for score, count in score_summary.items():
        bar = "#" * count
        print(f"    Score {score:>2}: {count:>2} scripts  {bar}")
    print()
    total_check = sum(score_summary.values())
    print(f"  Total: {total_check}")
    if missing:
        print(f"  WARNING: {len(missing)} script file(s) not found on disk.")
    else:
        print("  All script files loaded successfully.")
    print("=" * 50)


if __name__ == "__main__":
    main()
