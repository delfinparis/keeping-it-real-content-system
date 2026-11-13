#!/usr/bin/env python3
"""
One-time migration (2026-11-13): collapse duplicate episode files onto stable names.

Background: parse_rss.py used to name files by FEED POSITION (2026-10-28_item3_Kim-Rittberg).
Every new episode shifted every older one down a slot, so the daily sync saw "new" files,
re-transcribed and re-analyzed them, and left the old copies behind. Result: 1,060
transcripts for ~370 real episodes.

This script:
  1. Groups every stem by (publish date, guest) -- copies of one episode share both.
  2. Picks one canonical copy per group (has an analysis; then the newest copy).
  3. Renames it to the stable name from data/index/episodes.json (item<WordPress post ID>)
     when the episode is still in the RSS feed; episodes that have aged out of the 300-item
     feed keep their canonical name (they can no longer shift).
  4. Deletes the other copies (transcripts, analyses, clips, scripts, webapp copies).
  5. Rewrites stem references inside the JSON maps / reports / webapp, de-duplicating.
  6. Rebuilds progress.json so the sync knows what is already done.
  7. Writes data/index/stem_migration_map.json (old stem -> new stem) so other repos
     (video-strategy carousel state, kir-ai-seo) can migrate their references.

Run AFTER the new parse_rss.py has regenerated episodes.json:
    python scripts/parse_rss.py && python scripts/migrate_stable_ids.py [--dry-run]
"""

import argparse
import collections
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = ROOT / "data" / "transcripts"
ANALYSIS = ROOT / "data" / "analysis"
INDEX = ROOT / "data" / "index"
CLIPS = ROOT / "content" / "clips"
SCRIPTS = ROOT / "content" / "scripts"
WEB_DATA = ROOT / "webapp" / "src" / "data"
WEB_CLIPS = WEB_DATA / "clips"
WEB_ANALYSIS = WEB_DATA / "analysis"

STEM_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_(?:item|ep)(\d+)_(.+)$")

# Files that mention stems in their text and need references rewritten.
TEXT_FILES = [
    ROOT / "content" / "problem-map" / "problem_episode_map.json",
    ROOT / "content" / "avatars" / "avatar_episode_map.json",
    ROOT / "content" / "publish_ready.json",
    *sorted((ROOT / "content" / "kill_judge_reports").glob("*.json")),
    WEB_DATA / "all_analysis.json",
    ROOT / "webapp" / "src" / "app" / "clips" / "page.tsx",
]


def parse(stem):
    m = STEM_RE.match(stem)
    return (m.group(1), m.group(3), int(m.group(2))) if m else None


def stems_in(directory, suffix):
    out = {}
    for p in directory.glob(f"*{suffix}"):
        stem = p.name[: -len(suffix)]
        if parse(stem):
            out.setdefault(stem, []).append(p)
    return out


def script_files():
    """content/scripts/<stem>_<variant>.json -> {stem: {variant: path}}"""
    out = collections.defaultdict(dict)
    for p in SCRIPTS.glob("*.json"):
        m = re.match(r"^(\d{4}-\d{2}-\d{2}_(?:item|ep)\d+_.+?)_((?:clip\d+_v\d+|scripts)\.json)$", p.name)
        if m:
            out[m.group(1)][m.group(2)] = p
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    episodes = json.load(open(INDEX / "episodes.json"))["episodes"]
    feed_target = {}
    for ep in episodes:
        st = Path(ep["filename"]).stem
        d, g, _ = parse(st)
        assert (d, g) not in feed_target, f"two feed episodes share date+guest: {d} {g}"
        feed_target[(d, g)] = st

    transcripts = stems_in(TRANSCRIPTS, ".txt")
    transcript_json = stems_in(TRANSCRIPTS, ".json")
    analyses = stems_in(ANALYSIS, "_analysis.json")
    clips = stems_in(CLIPS, "_clips.json")
    web_clips = stems_in(WEB_CLIPS, "_clips.json")
    scripts = script_files()

    all_stems = set(transcripts) | set(transcript_json) | set(analyses) | set(clips) | set(web_clips) | set(scripts)
    groups = collections.defaultdict(list)
    for s in all_stems:
        d, g, _ = parse(s)
        groups[(d, g)].append(s)

    mapping = {}
    deletes, moves = [], []
    for key, members in groups.items():
        # Canonical copy: has an analysis, has a transcript, then the newest copy (highest
        # feed-position number = most recently generated).
        members.sort(key=lambda s: (s in analyses, s in transcripts, parse(s)[2]), reverse=True)
        canon = members[0]
        target = feed_target.get(key, canon)
        for s in members:
            mapping[s] = target

        def settle(index, suffix, directory):
            """Keep the best member's file for this kind, renamed to target; delete the rest."""
            have = [s for s in members if s in index]
            if not have:
                return
            keep = have[0]  # members already sorted by preference
            for s in have:
                for p in index[s]:
                    if s == keep:
                        dst = directory / f"{target}{suffix}"
                        if p != dst:
                            moves.append((p, dst))
                    else:
                        deletes.append(p)

        settle(transcripts, ".txt", TRANSCRIPTS)
        settle(transcript_json, ".json", TRANSCRIPTS)
        settle(analyses, "_analysis.json", ANALYSIS)
        settle(clips, "_clips.json", CLIPS)
        settle(web_clips, "_clips.json", WEB_CLIPS)
        variants = {v for s in members for v in scripts.get(s, {})}
        for v in variants:
            have = [s for s in members if v in scripts.get(s, {})]
            for s in have:
                p = scripts[s][v]
                if s == have[0]:
                    dst = SCRIPTS / f"{target}_{v}"
                    if p != dst:
                        moves.append((p, dst))
                else:
                    deletes.append(p)

    changed = {s: t for s, t in mapping.items() if s != t}
    print(f"episodes (groups): {len(groups)}")
    print(f"stems found: {len(all_stems)} -> {len(set(mapping.values()))} after migration")
    print(f"files to delete: {len(deletes)}   files to rename: {len(moves)}")
    print(f"transcripts: {len(transcripts)} -> {len({mapping[s] for s in transcripts})}")
    print(f"analyses:    {len(analyses)} -> {len({mapping[s] for s in analyses})}")
    if args.dry_run:
        for p, d in moves[:5]:
            print("  mv", p.name, "->", d.name)
        return

    # Deletes first, then moves (a move target can be another member's old path).
    for p in deletes:
        p.unlink()
    staged = []
    for p, dst in moves:
        tmp = p.with_name(p.name + ".migrating")
        p.rename(tmp)
        staged.append((tmp, dst))
    for tmp, dst in staged:
        assert not dst.exists(), f"refusing to overwrite {dst}"
        tmp.rename(dst)

    # Fix embedded source_file fields.
    for p in TRANSCRIPTS.glob("*.json"):
        t = json.load(open(p))
        if t.get("source_file") != p.stem + ".mp3":
            t["source_file"] = p.stem + ".mp3"
            json.dump(t, open(p, "w"), indent=2, ensure_ascii=False)
    for p in ANALYSIS.glob("*_analysis.json"):
        a = json.load(open(p))
        stem = p.name[: -len("_analysis.json")]
        if a.get("_metadata", {}).get("source_file") not in (None, stem):
            a["_metadata"]["source_file"] = stem
            json.dump(a, open(p, "w"), indent=2, ensure_ascii=False)

    # Rewrite stem references in text files (longest stems first so item1 never eats item10).
    if changed:
        pat = re.compile(
            "(" + "|".join(re.escape(s) for s in sorted(changed, key=len, reverse=True)) + r")(?![A-Za-z0-9.'\-])"
        )
        for f in TEXT_FILES:
            if f.exists():
                txt = f.read_text()
                new = pat.sub(lambda m: changed[m.group(1)], txt)
                if new != txt:
                    f.write_text(new)

    # De-duplicate the maps (same episode now appears once per copy).
    pm_path = ROOT / "content" / "problem-map" / "problem_episode_map.json"
    pm = json.load(open(pm_path))
    for cat, problems in pm.items():
        for prob, entries in problems.items():
            seen, out = set(), []
            for e in entries:
                if e.get("episode") not in seen:
                    seen.add(e.get("episode"))
                    out.append(e)
            problems[prob] = out
    json.dump(pm, open(pm_path, "w"), indent=2, ensure_ascii=False)

    am_path = ROOT / "content" / "avatars" / "avatar_episode_map.json"
    am = json.load(open(am_path))
    for av, entries in am.items():
        seen, out = set(), []
        for e in entries:
            if e.get("episode") not in seen:
                seen.add(e.get("episode"))
                out.append(e)
        am[av] = out
    json.dump(am, open(am_path, "w"), indent=2, ensure_ascii=False)

    aa_path = WEB_DATA / "all_analysis.json"
    if aa_path.exists():
        aa = json.load(open(aa_path))
        if isinstance(aa, list):
            seen, out = set(), []
            for a in aa:
                k = a.get("_metadata", {}).get("source_file")
                if k is None or k not in seen:
                    seen.add(k)
                    out.append(a)
            json.dump(out, open(aa_path, "w"), indent=2, ensure_ascii=False)

    # Webapp copies: mirror content/ and data/analysis exactly.
    shutil.copy2(pm_path, WEB_DATA / "problem_episode_map.json")
    shutil.copy2(am_path, WEB_DATA / "avatar_episode_map.json")
    for p in WEB_ANALYSIS.glob("*_analysis.json"):
        p.unlink()
    for p in ANALYSIS.glob("*_analysis.json"):
        shutil.copy2(p, WEB_ANALYSIS / p.name)

    # Progress: every feed episode that already has a transcript is done.
    have = {p.stem for p in TRANSCRIPTS.glob("*.txt")}
    done = [ep["filename"] for ep in episodes if Path(ep["filename"]).stem in have]
    prog_path = INDEX / "progress.json"
    prog = json.load(open(prog_path))
    prog["downloaded"] = done
    prog["transcribed"] = done
    json.dump(prog, open(prog_path, "w"), indent=2)

    # Old -> new map for other repos.
    json.dump(dict(sorted(changed.items())), open(INDEX / "stem_migration_map.json", "w"), indent=1)
    print(f"done. feed episodes still needing a transcript: {len(episodes) - len(done)}")


if __name__ == "__main__":
    main()
