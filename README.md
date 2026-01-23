# Keeping It Real Podcast - Content Intelligence System

Transform 700+ episodes of "Keeping It Real Podcast" into a searchable content library and recruitment tool for Kale Realty.

## Overview

This system provides:
- **Episode Index**: Searchable metadata for all podcast episodes
- **Transcripts**: Full transcripts with timestamps for all episodes
- **Problem-Solution Mapping**: Episodes tagged by agent challenges they address
- **Clip Extraction**: Identify 60-second clip-worthy moments for social media
- **Recruitment Tool**: Match agent pain points to relevant episodes instantly

## Project Structure

```
keeping-it-real-content-system/
├── data/
│   ├── index/
│   │   ├── episodes.json   # Master episode list with metadata
│   │   ├── episodes.csv    # Spreadsheet-friendly version
│   │   └── progress.json   # Processing status tracker
│   ├── transcripts/        # Whisper output with timestamps
│   ├── analysis/           # AI-extracted insights per episode
│   └── raw/mp3/            # Audio files (gitignored)
├── content/
│   ├── clips/              # Clip-worthy moments with timestamps
│   ├── scripts/            # 60-second video scripts
│   ├── problem-map/        # Problems → Episodes mapping
│   └── avatars/            # Agent avatar profiles & their episodes
├── scripts/
│   ├── parse_rss.py        # RSS feed parser
│   ├── download_episodes.py # Episode downloader with resume
│   └── transcribe_episodes.py # Whisper transcription
├── webapp/                 # React/Next.js recommendation app (coming)
└── docs/
    ├── AGENT_PROBLEMS.md   # Comprehensive problem taxonomy
    └── CONTENT_STRATEGY.md # Video content calendar & strategy
```

## Quick Start

### Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Phase 1: Download Episodes

```bash
# Parse RSS feed and create episode index
python scripts/parse_rss.py

# Download episodes (all or limited)
python scripts/download_episodes.py --limit 10  # First 10
python scripts/download_episodes.py             # All episodes

# Check download status
python scripts/download_episodes.py --status
```

### Phase 2: Transcribe Episodes

```bash
# Transcribe with Whisper (base model recommended)
python scripts/transcribe_episodes.py --model base --limit 5

# Use larger model for better quality (slower)
python scripts/transcribe_episodes.py --model medium

# Check transcription status
python scripts/transcribe_episodes.py --status
```

## Whisper Models

| Model  | Size   | Speed    | Quality  | Use Case |
|--------|--------|----------|----------|----------|
| tiny   | 39 MB  | Fastest  | Lower    | Quick test |
| base   | 74 MB  | Fast     | Good     | Default |
| small  | 244 MB | Medium   | Better   | Production |
| medium | 769 MB | Slower   | High     | High quality |
| large  | 1550 MB| Slowest  | Highest  | Best quality |

## Progress Tracking

The system tracks progress in `data/index/progress.json`:
- `downloaded`: Episodes with MP3 files
- `transcribed`: Episodes with completed transcripts
- `analyzed`: Episodes with AI analysis

## Requirements

- Python 3.9+
- ffmpeg (for audio processing)
- ~50GB disk space for full catalog download
- ~5-10 hours for full transcription (depending on hardware)

## License

Private - Kale Realty Internal Use
