#!/usr/bin/env python3
"""
Parse the Keeping It Real Podcast RSS feed and extract episode metadata.
"""

import feedparser
import json
import csv
import re
from datetime import datetime
from dateutil import parser as date_parser
from pathlib import Path

RSS_URL = "https://keepingitrealpod.com/feed/podcast"
DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_DIR = DATA_DIR / "index"

def parse_guest_from_title(title):
    """
    Extract guest name from episode title.
    Common patterns for this podcast:
    - "Topic • Guest Name" (most common)
    - "Topic • Guest Name • More Info"
    - "Guest Name talks about..."
    """
    # Pattern: "Topic • Guest Name" - guest is after the bullet
    if '•' in title:
        parts = [p.strip() for p in title.split('•')]
        # The guest name is typically the last part that looks like a name
        for part in reversed(parts):
            # Check if it looks like a name (1-4 capitalized words, may include periods for initials)
            if re.match(r'^[A-Z][a-zA-Z\.]+(?:\s+[A-Z][a-zA-Z\.]+){0,3}$', part):
                return part
        # If no match in reversed, try the second part (common pattern: Topic • Guest Name)
        if len(parts) >= 2:
            second = parts[1].strip()
            # Be more lenient - if it's 2-4 words and starts with capital
            words = second.split()
            if 1 <= len(words) <= 4 and words[0][0].isupper():
                return second

    # Pattern: "Name - Topic"
    if ' - ' in title:
        parts = title.split(' - ')
        first_part = parts[0].strip()
        if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}$', first_part):
            return first_part

    # Pattern: "Name: Topic"
    if ': ' in title:
        parts = title.split(': ')
        first_part = parts[0].strip()
        if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}$', first_part):
            return first_part

    return None

def parse_episode_number(title, item):
    """Extract episode number from title or item metadata."""
    # Try from itunes:episode
    if hasattr(item, 'itunes_episode'):
        return item.itunes_episode

    # Try from title
    match = re.search(r'(?:Episode|Ep\.?|#)\s*(\d+)', title, re.IGNORECASE)
    if match:
        return match.group(1)

    return None

def get_duration_seconds(item):
    """Extract duration in seconds from item."""
    if hasattr(item, 'itunes_duration'):
        duration = item.itunes_duration
        if ':' in str(duration):
            parts = str(duration).split(':')
            if len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            elif len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
        else:
            try:
                return int(duration)
            except:
                pass
    return None

def get_mp3_url(item):
    """Extract MP3 URL from enclosures."""
    if hasattr(item, 'enclosures') and item.enclosures:
        for enc in item.enclosures:
            if enc.get('type', '').startswith('audio/') or enc.get('href', '').endswith('.mp3'):
                return enc.get('href')
    if hasattr(item, 'links'):
        for link in item.links:
            if link.get('type', '').startswith('audio/') or link.get('href', '').endswith('.mp3'):
                return link.get('href')
    return None

def sanitize_filename(name):
    """Create a safe filename from a string."""
    if not name:
        return "unknown"
    # Remove or replace unsafe characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '-', name)
    name = name.strip('-')
    return name[:50]  # Limit length

def parse_rss_feed():
    """Parse the RSS feed and return episode data."""
    print(f"Fetching RSS feed from {RSS_URL}...")
    feed = feedparser.parse(RSS_URL)

    if feed.bozo and feed.bozo_exception:
        print(f"Warning: Feed parsing had issues: {feed.bozo_exception}")

    print(f"Feed title: {feed.feed.get('title', 'Unknown')}")
    print(f"Total items found: {len(feed.entries)}")

    episodes = []
    has_transcript = 0

    for i, item in enumerate(feed.entries):
        title = item.get('title', 'Untitled')

        # Parse publish date
        pub_date = None
        pub_date_str = None
        if hasattr(item, 'published'):
            try:
                pub_date = date_parser.parse(item.published)
                pub_date_str = pub_date.strftime('%Y-%m-%d')
            except:
                pub_date_str = item.published

        # Extract metadata
        guest_name = parse_guest_from_title(title)
        episode_number = parse_episode_number(title, item)
        mp3_url = get_mp3_url(item)
        duration_seconds = get_duration_seconds(item)
        description = item.get('summary', item.get('description', ''))

        # Check for embedded transcript
        transcript = None
        if hasattr(item, 'content'):
            for content in item.content:
                if 'transcript' in content.get('type', '').lower():
                    transcript = content.get('value', '')
                    has_transcript += 1

        # Generate filename
        date_part = pub_date_str if pub_date_str else 'unknown-date'
        ep_part = f"ep{episode_number}" if episode_number else f"item{i+1}"
        guest_part = sanitize_filename(guest_name) if guest_name else 'unknown-guest'
        filename = f"{date_part}_{ep_part}_{guest_part}.mp3"

        episode = {
            'id': i + 1,
            'title': title,
            'guest_name': guest_name,
            'episode_number': episode_number,
            'publish_date': pub_date_str,
            'description': description[:500] + '...' if len(description) > 500 else description,
            'full_description': description,
            'mp3_url': mp3_url,
            'duration_seconds': duration_seconds,
            'duration_formatted': f"{duration_seconds // 3600}:{(duration_seconds % 3600) // 60:02d}:{duration_seconds % 60:02d}" if duration_seconds else None,
            'filename': filename,
            'has_transcript': transcript is not None,
            'guid': item.get('id', item.get('guid', '')),
        }
        episodes.append(episode)

    print(f"\nEpisodes with embedded transcripts: {has_transcript}")

    return episodes, feed.feed

def save_episodes(episodes, feed_info):
    """Save episodes to JSON and CSV formats."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # Save as JSON
    json_path = INDEX_DIR / "episodes.json"
    output = {
        'feed_title': feed_info.get('title', ''),
        'feed_description': feed_info.get('description', ''),
        'feed_link': feed_info.get('link', ''),
        'total_episodes': len(episodes),
        'generated_at': datetime.now().isoformat(),
        'episodes': episodes
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to {json_path}")

    # Save as CSV (without full_description to keep it manageable)
    csv_path = INDEX_DIR / "episodes.csv"
    csv_fields = ['id', 'title', 'guest_name', 'episode_number', 'publish_date',
                  'duration_formatted', 'mp3_url', 'filename', 'has_transcript']
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(episodes)
    print(f"Saved CSV to {csv_path}")

    # Initialize progress tracker
    progress_path = INDEX_DIR / "progress.json"
    progress = {
        'total_episodes': len(episodes),
        'downloaded': [],
        'transcribed': [],
        'analyzed': [],
        'last_updated': datetime.now().isoformat()
    }
    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)
    print(f"Initialized progress tracker at {progress_path}")

    return json_path, csv_path

def print_sample_episodes(episodes, n=5):
    """Print sample episodes for verification."""
    print(f"\n{'='*60}")
    print(f"SAMPLE OF FIRST {n} EPISODES:")
    print('='*60)
    for ep in episodes[:n]:
        print(f"\n[{ep['id']}] {ep['title']}")
        print(f"    Guest: {ep['guest_name'] or 'Unknown'}")
        print(f"    Date: {ep['publish_date']}")
        print(f"    Episode #: {ep['episode_number'] or 'Unknown'}")
        print(f"    Duration: {ep['duration_formatted'] or 'Unknown'}")
        print(f"    Filename: {ep['filename']}")
        print(f"    MP3 URL: {ep['mp3_url'][:80]}..." if ep['mp3_url'] and len(ep['mp3_url']) > 80 else f"    MP3 URL: {ep['mp3_url']}")

if __name__ == "__main__":
    episodes, feed_info = parse_rss_feed()
    json_path, csv_path = save_episodes(episodes, feed_info)
    print_sample_episodes(episodes)

    # Summary stats
    print(f"\n{'='*60}")
    print("SUMMARY:")
    print('='*60)
    print(f"Total episodes: {len(episodes)}")
    print(f"Episodes with guest names parsed: {sum(1 for e in episodes if e['guest_name'])}")
    print(f"Episodes with MP3 URLs: {sum(1 for e in episodes if e['mp3_url'])}")
    print(f"Episodes with durations: {sum(1 for e in episodes if e['duration_seconds'])}")

    # Date range
    dates = [e['publish_date'] for e in episodes if e['publish_date']]
    if dates:
        print(f"Date range: {min(dates)} to {max(dates)}")
