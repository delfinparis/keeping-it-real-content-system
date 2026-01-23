#!/usr/bin/env python3
"""
Download podcast episodes with resume capability and progress tracking.
"""

import json
import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import hashlib

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_DIR = DATA_DIR / "index"
MP3_DIR = DATA_DIR / "raw" / "mp3"

def load_episodes():
    """Load episode index."""
    json_path = INDEX_DIR / "episodes.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['episodes']

def load_progress():
    """Load download progress."""
    progress_path = INDEX_DIR / "progress.json"
    with open(progress_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(progress):
    """Save download progress."""
    progress_path = INDEX_DIR / "progress.json"
    progress['last_updated'] = datetime.now().isoformat()
    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def get_file_size(url, timeout=30):
    """Get file size from URL headers."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return int(response.headers.get('content-length', 0))
    except:
        return 0

def download_file(url, filepath, expected_size=None):
    """
    Download a file with progress bar and resume support.
    Returns (success, actual_size, error_message)
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Check if file already exists and is complete
    if filepath.exists():
        existing_size = filepath.stat().st_size
        if expected_size and existing_size == expected_size:
            return True, existing_size, "Already downloaded"
        elif expected_size and existing_size > expected_size * 0.95:
            # Allow 5% tolerance for size differences
            return True, existing_size, "Already downloaded (size within tolerance)"

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        with open(filepath, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True,
                     desc=filepath.name[:40], leave=False) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        actual_size = filepath.stat().st_size
        return True, actual_size, None

    except requests.exceptions.RequestException as e:
        return False, 0, str(e)
    except Exception as e:
        return False, 0, str(e)

def verify_file(filepath, min_size_mb=1):
    """
    Verify file integrity (basic check - file exists and has reasonable size).
    """
    filepath = Path(filepath)
    if not filepath.exists():
        return False, "File does not exist"

    size_mb = filepath.stat().st_size / (1024 * 1024)
    if size_mb < min_size_mb:
        return False, f"File too small ({size_mb:.1f} MB < {min_size_mb} MB)"

    return True, f"OK ({size_mb:.1f} MB)"

def download_episodes(limit=None, start_from=0, verify=True):
    """
    Download episodes with resume capability.

    Args:
        limit: Maximum number of episodes to download (None = all)
        start_from: Episode index to start from (0-based)
        verify: Whether to verify downloaded files
    """
    episodes = load_episodes()
    progress = load_progress()

    MP3_DIR.mkdir(parents=True, exist_ok=True)

    # Filter to episodes that need downloading
    to_download = []
    for i, ep in enumerate(episodes):
        if i < start_from:
            continue
        if ep['filename'] in progress['downloaded']:
            continue
        if not ep['mp3_url']:
            continue
        to_download.append(ep)
        if limit and len(to_download) >= limit:
            break

    if not to_download:
        print("No episodes to download.")
        return

    print(f"\nDownloading {len(to_download)} episodes...")
    print(f"Destination: {MP3_DIR}\n")

    success_count = 0
    fail_count = 0
    skip_count = 0

    for ep in tqdm(to_download, desc="Overall progress"):
        filepath = MP3_DIR / ep['filename']

        # Download
        success, size, error = download_file(ep['mp3_url'], filepath)

        if success:
            if verify:
                valid, msg = verify_file(filepath)
                if not valid:
                    print(f"\n  Warning: {ep['filename']} - {msg}")
                    fail_count += 1
                    continue

            # Update progress
            progress['downloaded'].append(ep['filename'])
            save_progress(progress)
            success_count += 1

            if error == "Already downloaded" or "tolerance" in str(error):
                skip_count += 1
        else:
            print(f"\n  Failed: {ep['filename']} - {error}")
            fail_count += 1

    print(f"\n{'='*60}")
    print(f"Download complete!")
    print(f"  Successful: {success_count}")
    print(f"  Skipped (already had): {skip_count}")
    print(f"  Failed: {fail_count}")
    print(f"  Total downloaded so far: {len(progress['downloaded'])}")
    print(f"{'='*60}")

def show_status():
    """Show current download status."""
    episodes = load_episodes()
    progress = load_progress()

    total = len(episodes)
    downloaded = len(progress['downloaded'])
    remaining = total - downloaded

    # Calculate total size of downloaded files
    total_size = 0
    for filename in progress['downloaded']:
        filepath = MP3_DIR / filename
        if filepath.exists():
            total_size += filepath.stat().st_size

    print(f"\n{'='*60}")
    print("DOWNLOAD STATUS")
    print(f"{'='*60}")
    print(f"Total episodes in index: {total}")
    print(f"Downloaded: {downloaded}")
    print(f"Remaining: {remaining}")
    print(f"Total size downloaded: {total_size / (1024**3):.2f} GB")
    print(f"Last updated: {progress.get('last_updated', 'Never')}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download podcast episodes")
    parser.add_argument('--limit', '-l', type=int, default=None,
                       help='Limit number of episodes to download')
    parser.add_argument('--start', '-s', type=int, default=0,
                       help='Start from episode index (0-based)')
    parser.add_argument('--status', action='store_true',
                       help='Show download status only')
    parser.add_argument('--no-verify', action='store_true',
                       help='Skip file verification')

    args = parser.parse_args()

    if args.status:
        show_status()
    else:
        download_episodes(
            limit=args.limit,
            start_from=args.start,
            verify=not args.no_verify
        )
