#!/usr/bin/env python3
"""
Auto-Sync Script for Keeping It Real Podcast
Checks RSS feed for new episodes, downloads, transcribes, and analyzes them.

Run weekly via cron: 0 3 * * 0 cd /path/to/project && ./scripts/auto_sync.py

Or manually: python scripts/auto_sync.py
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"
WEBAPP_DIR = PROJECT_ROOT / "webapp"
WEBAPP_DATA_DIR = WEBAPP_DIR / "src" / "data"
INDEX_DIR = DATA_DIR / "index"
ANALYSIS_DIR = DATA_DIR / "analysis"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"

# Ensure we're using the project's venv
VENV_PYTHON = PROJECT_ROOT / "venv" / "bin" / "python"


def run_script(script_name: str, args: list = None, env: dict = None) -> tuple[bool, str]:
    """Run a Python script from the scripts directory."""
    script_path = SCRIPTS_DIR / script_name
    cmd = [str(VENV_PYTHON), str(script_path)]
    if args:
        cmd.extend(args)

    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            env=full_env,
            timeout=3600  # 1 hour timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Script timed out after 1 hour"
    except Exception as e:
        return False, str(e)


def get_current_episode_count() -> int:
    """Get the number of episodes currently in the index."""
    episodes_file = INDEX_DIR / "episodes.json"
    if episodes_file.exists():
        with open(episodes_file, 'r') as f:
            data = json.load(f)
            return data.get('total_episodes', 0)
    return 0


def get_progress() -> dict:
    """Get the current progress from progress.json."""
    progress_file = INDEX_DIR / "progress.json"
    if progress_file.exists():
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {'downloaded': 0, 'transcribed': 0, 'analyzed': 0}


def sync_to_webapp():
    """Copy updated data files to the webapp."""
    logger.info("Syncing data to webapp...")

    # Copy episodes.json
    src = INDEX_DIR / "episodes.json"
    dst = WEBAPP_DATA_DIR / "episodes.json"
    if src.exists():
        shutil.copy2(src, dst)
        logger.info(f"  Copied {src.name}")

    # Copy problem_episode_map.json
    src = PROJECT_ROOT / "content" / "problem-map" / "problem_episode_map.json"
    dst = WEBAPP_DATA_DIR / "problem_episode_map.json"
    if src.exists():
        shutil.copy2(src, dst)
        logger.info(f"  Copied {src.name}")

    # Copy avatar_episode_map.json
    src = PROJECT_ROOT / "content" / "avatars" / "avatar_episode_map.json"
    dst = WEBAPP_DATA_DIR / "avatar_episode_map.json"
    if src.exists():
        shutil.copy2(src, dst)
        logger.info(f"  Copied {src.name}")

    # Copy analysis files
    analysis_dst = WEBAPP_DATA_DIR / "analysis"
    analysis_dst.mkdir(exist_ok=True)
    for analysis_file in ANALYSIS_DIR.glob("*_analysis.json"):
        shutil.copy2(analysis_file, analysis_dst / analysis_file.name)
    logger.info(f"  Copied {len(list(ANALYSIS_DIR.glob('*_analysis.json')))} analysis files")


def main():
    """Main sync workflow."""
    logger.info("=" * 60)
    logger.info("Starting auto-sync at %s", datetime.now().isoformat())
    logger.info("=" * 60)

    # Check for API key
    openai_key = os.environ.get('OPENAI_API_KEY')
    if not openai_key:
        # Try to read from webapp .env.local
        env_file = WEBAPP_DIR / ".env.local"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('OPENAI_API_KEY='):
                        openai_key = line.strip().split('=', 1)[1]
                        break

    if not openai_key:
        logger.error("No OPENAI_API_KEY found. Analysis will be skipped.")

    # Step 1: Parse RSS feed to check for new episodes
    logger.info("\n[STEP 1] Checking RSS feed for new episodes...")
    old_count = get_current_episode_count()

    success, output = run_script("parse_rss.py")
    if not success:
        logger.error("Failed to parse RSS feed: %s", output)
        return 1

    new_count = get_current_episode_count()
    new_episodes = new_count - old_count

    if new_episodes > 0:
        logger.info(f"  Found {new_episodes} new episode(s)!")
    else:
        logger.info("  No new episodes found.")

    # Step 2: Download new episodes
    logger.info("\n[STEP 2] Downloading new episodes...")
    progress_before = get_progress()

    # Download any not yet downloaded (limit to 10 per run to avoid overload)
    success, output = run_script("download_episodes.py", ["--limit", "10"])
    if not success:
        logger.warning("Download had issues: %s", output[-500:])

    progress_after = get_progress()
    downloaded = progress_after.get('downloaded', 0) - progress_before.get('downloaded', 0)
    logger.info(f"  Downloaded {downloaded} episode(s)")

    # Step 3: Transcribe new episodes
    logger.info("\n[STEP 3] Transcribing new episodes...")
    transcribed_before = progress_before.get('transcribed', 0)

    success, output = run_script("transcribe_episodes.py")
    if not success:
        logger.warning("Transcription had issues: %s", output[-500:])

    progress_after = get_progress()
    transcribed = progress_after.get('transcribed', 0) - transcribed_before
    logger.info(f"  Transcribed {transcribed} episode(s)")

    # Step 4: Analyze new transcripts (if API key available)
    if openai_key:
        logger.info("\n[STEP 4] Analyzing new transcripts...")
        analyzed_before = progress_before.get('analyzed', 0)

        success, output = run_script(
            "analyze_episodes.py",
            ["--provider", "openai", "--generate-scripts"],
            env={"OPENAI_API_KEY": openai_key}
        )
        if not success:
            logger.warning("Analysis had issues: %s", output[-500:])

        progress_after = get_progress()
        analyzed = progress_after.get('analyzed', 0) - analyzed_before
        logger.info(f"  Analyzed {analyzed} episode(s)")
    else:
        logger.info("\n[STEP 4] Skipping analysis (no API key)")

    # Step 5: Sync data to webapp
    logger.info("\n[STEP 5] Syncing data to webapp...")
    sync_to_webapp()

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("AUTO-SYNC COMPLETE")
    logger.info("=" * 60)

    final_progress = get_progress()
    logger.info(f"Total episodes in catalog: {get_current_episode_count()}")
    logger.info(f"Downloaded: {final_progress.get('downloaded', 0)}")
    logger.info(f"Transcribed: {final_progress.get('transcribed', 0)}")
    logger.info(f"Analyzed: {final_progress.get('analyzed', 0)}")
    logger.info("")
    logger.info("Webapp data updated. Restart/redeploy webapp to see changes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
