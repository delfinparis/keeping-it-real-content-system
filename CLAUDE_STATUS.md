# Project Status - Keeping It Real Content System

**Last Updated:** 2026-04-28
**GitHub:** <https://github.com/delfinparis/keeping-it-real-content-system>

---

## Current State (2026-04-28)

Active workstream: **Voice Corpus build** to feed a future "D.J. Voice Signatures" section in the editorial standards. RSS was re-parsed and 30 most-recent MP3s downloaded earlier today on another device (commit `fd5eb36`); transcription is the next step and is being handled from a separate device tonight. See [`docs/VOICE_CORPUS_HANDOFF.md`](docs/VOICE_CORPUS_HANDOFF.md) for the resume instructions.

The weekly auto-sync GitHub Action had been failing every Sunday since at least 2026-02-22 due to a hardcoded `venv/bin/python` path that doesn't exist on the CI runner. Fixed 2026-04-28 (this session); next scheduled run Sun 2026-05-03 03:00 UTC.

### On-disk pipeline state (this machine)

| Metric                                | Count      | Notes |
| ------------------------------------- | ---------: | ----- |
| Episodes in catalog (`episodes.json`) | 300        | Re-parsed 2026-04-28; latest episode 2026-04-27 |
| MP3 files on this machine             | 2          | The 30 new MP3s downloaded today live on a different device (gitignored, won't sync) |
| Unique transcripts (basename)         | 595        | See "known data quirk" below |
| Unique analyses (basename)            | 595        | Same |
| Most recent transcript / analysis     | 2026-01-30 | Amanda Pendleton — pre-Voice-Corpus |

### Known data quirk

`scripts/parse_rss.py` numbers episodes `item1` = newest at parse time. Each re-parse renumbers, so the same episode appears under multiple `itemN` filenames (item3 / item4 / etc. each appear 3x in `data/transcripts/`). The 595 unique-basename count therefore inflates above the 300 actual catalog count. Cleanup task: dedupe by `guid` rather than filename. Not blocking — just inflates counters.

---

## Completed Phases

| Phase | Status |
|-------|--------|
| 1 — Infrastructure (RSS, downloader, dirs) | done |
| 2 — Transcription (Whisper) | done through 2026-01-30; 30-episode catch-up batch in flight |
| 3 — Content Analysis (problems, avatars, scripts) | done through 2026-01-30; awaits new transcripts |
| 4 — Web App (Next.js + GPT-4o-mini recommender) | done |
| 5 — Documentation (AGENT_PROBLEMS, CONTENT_STRATEGY) | done |
| 6 — Auto-sync (weekly GH Action) | fixed 2026-04-28 — was broken Feb–Apr 2026 |

### Avatar coverage (Jan 2026 snapshot)

| Avatar                | Episodes |
|-----------------------|----------|
| Aspiring Top Producer | 130      |
| Team Leader           | 48       |
| Overwhelmed Newbie    | 41       |
| Stuck Intermediate    | 35       |
| Burned-Out Veteran    | 16       |
| Forgotten Middle      | 1        |

These counts are pre-2026-01-30. Re-run avatar mapping after the Voice Corpus transcripts land.

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/parse_rss.py` | Parse RSS feed, create episode index |
| `scripts/download_episodes.py` | Download MP3s with resume |
| `scripts/transcribe_episodes.py` | Whisper transcription |
| `scripts/analyze_episodes.py` | AI analysis (OpenAI/Anthropic) |
| `scripts/auto_sync.py` | Weekly orchestrator (RSS → download → transcribe → analyze → webapp) |
| `.github/workflows/weekly-sync.yml` | Sun 03:00 UTC cron — fires `auto_sync.py` |
| `data/index/episodes.json` | Master index (300 episodes through 2026-04-27) |
| `data/index/progress.json` | Pipeline progress (rebuilt 2026-04-28 by `parse_rss.py`) |
| `content/problem-map/problem_episode_map.json` | Problems → Episodes |
| `content/avatars/avatar_episode_map.json` | Avatars → Episodes |
| `docs/VOICE_CORPUS_HANDOFF.md` | Resume instructions for the in-flight Voice Corpus build |

---

## To Continue

### Voice Corpus build (active)

See [`docs/VOICE_CORPUS_HANDOFF.md`](docs/VOICE_CORPUS_HANDOFF.md). Short version: the device that ran today's download has the 30 MP3s in `data/raw/mp3/`; run `transcribe_episodes.py --limit 30` there, commit the resulting `data/transcripts/2026-*.{txt,json}` files, push.

### General pipeline catch-up

```bash
# Re-parse RSS for new episodes
source venv/bin/activate
python scripts/parse_rss.py

# Download any new ones
python scripts/download_episodes.py

# Transcribe new MP3s
python scripts/transcribe_episodes.py

# Analyze (OpenAI key required)
OPENAI_API_KEY="..." python scripts/analyze_episodes.py --provider openai --generate-scripts
```

Or trigger the workflow manually (now that it's fixed):

```bash
gh workflow run weekly-sync.yml
```

### Run the web app

```bash
cd webapp
npm install
npm run dev      # http://localhost:3000
```

---

## API Keys Needed

- **OpenAI**: `OPENAI_API_KEY` (used for analysis; stored as `OPENAI_API_KEY` GitHub secret for CI)
- **Anthropic**: `ANTHROPIC_API_KEY` (alternative provider)

---

## Project Brief Location

Full project requirements: `/Users/djparis/Downloads/podcast_project_brief.md`

---

## Commands Cheat Sheet

```bash
# Status of each pipeline stage
python scripts/analyze_episodes.py --status
python scripts/download_episodes.py --status
python scripts/transcribe_episodes.py --status

# Run a specific episode
OPENAI_API_KEY="..." python scripts/analyze_episodes.py --episode "filename" --provider openai

# Trigger the weekly sync manually
gh workflow run weekly-sync.yml

# Watch latest workflow run
gh run watch
```
