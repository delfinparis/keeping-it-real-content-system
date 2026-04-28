# Voice Corpus Build — Handoff

**Started:** 2026-04-28 (this session)
**Goal:** Add the last 30 KIR episodes to the existing transcript pile (1,190 files in `data/transcripts/`) so we can build a "D.J. Voice Signatures" section in the editorial standards from a fresh corpus.

---

## State as of this commit

### Done

- **`scripts/parse_rss.py` re-run.** Episode index refreshed from the RSS feed at `https://keepingitrealpod.com/feed/podcast`. Index now reflects 300 total episodes, latest dated 2026-04-27. The diffs to `data/index/episodes.json`, `data/index/episodes.csv`, and `data/index/progress.json` are part of this commit.
- **`scripts/download_episodes.py --limit 30` completed successfully on this machine.** All 30 most-recent MP3s are sitting in `data/raw/mp3/` (~ 13 GB total). The downloads are gitignored per `.gitignore` (`data/raw/mp3/` and `*.mp3`), so they will NOT come down with a `git pull` on another device.

### Not done yet

- **Transcription has not been run on the 30 new MP3s.** This is the long step. Whisper at the `base` model on this hardware took roughly 5-10x realtime per episode, and KIR episodes average ~45 minutes. Expect the full transcribe pass to take 2-5 hours of compute, depending on the device.
- **Voice Signatures analysis has not been started.** That waits until after transcription completes.

---

## Resuming on another device tonight

### Path A: Same machine that already has the MP3s downloaded

If you are on the device that ran the download in this session (you know this is true if `data/raw/mp3/` has 13GB of recent files and `ls -t data/raw/mp3/ | head -3` shows files from 2026-04 or later):

```bash
cd "~/GitHub Projects/keeping-it-real-content-system"
/Users/djparis/kale_env/bin/python scripts/transcribe_episodes.py --limit 30
```

This processes the 30 newest MP3s into `data/transcripts/` as paired `.txt` and `.json` files. When it finishes, commit the new transcripts:

```bash
git add data/transcripts/2026-*.txt data/transcripts/2026-*.json
git commit -m "Add 30 most recent KIR episode transcripts (Voice Corpus build)"
git push origin main
```

### Path B: A different device that does not have the MP3s

The MP3s are gitignored so they won't sync via `git pull`. Re-download first:

```bash
cd "~/GitHub Projects/keeping-it-real-content-system"
git pull origin main

# Verify deps
/Users/djparis/kale_env/bin/pip install -q feedparser requests tqdm pandas python-dateutil openai-whisper

# Re-fetch the RSS index (idempotent — should already be current)
/Users/djparis/kale_env/bin/python scripts/parse_rss.py

# Download the 30 newest MP3s (~3-5 minutes)
/Users/djparis/kale_env/bin/python scripts/download_episodes.py --limit 30

# Transcribe (the long step — 2-5 hours)
/Users/djparis/kale_env/bin/python scripts/transcribe_episodes.py --limit 30

# Commit the transcripts when done
git add data/transcripts/2026-*.txt data/transcripts/2026-*.json
git commit -m "Add 30 most recent KIR episode transcripts (Voice Corpus build)"
git push origin main
```

### Tips for the long transcribe step

- It runs locally (uses the openai-whisper Python package, not the OpenAI API).
- You can leave it running overnight and check in the morning. There is no API cost or rate limit.
- If a transcription fails midway, `transcribe_episodes.py` skips already-transcribed files on re-run unless you pass `--force`.
- To speed up at the cost of accuracy, change the model: `--model tiny` is roughly 2x faster than `base`. For voice-pattern analysis, `base` is the sweet spot.

---

## What happens after transcription

Once the 30 new transcripts are in `data/transcripts/`, the next session does the analysis pass:

1. Pull D.J.'s lines only out of each transcript (strip guest dialogue).
2. Concatenate D.J.'s lines into a single voice-corpus file.
3. Extract recurring patterns: openers, closers, comparison structures, characteristic phrases, sentence rhythms, never-says, callbacks, story-telling shape.
4. Draft a new section -- **"D.J. Voice Signatures"** -- to be added to `video-strategy-to-grow-dj-brand/docs/editorial-standards.md` (the canonical voice doc).
5. Cross-reference the section from the other editorial docs that already inherit it (kale-download, sales-workflow webinar, KIR POLISH_PROMPTs).

That's the work to pick up next session.
