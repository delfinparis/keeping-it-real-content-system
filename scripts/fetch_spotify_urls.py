#!/usr/bin/env python3
"""
Fetch Spotify episode URLs for Keeping It Real podcast
"""

import json
import re
import time
from pathlib import Path
import subprocess

# Spotify show ID
SHOW_ID = "6lDHbQ8nfuV87QyqiELilc"
BASE_URL = f"https://open.spotify.com/show/{SHOW_ID}"

PROJECT_ROOT = Path(__file__).parent.parent
EPISODES_FILE = PROJECT_ROOT / "webapp/src/data/episodes.json"
OUTPUT_FILE = PROJECT_ROOT / "data/index/spotify_urls.json"

def fetch_spotify_page(offset=0):
    """Fetch episodes from Spotify (requires browser automation or API)"""
    # For now, we'll use a simple curl approach
    # This might not get all episodes due to JS rendering
    import urllib.request

    url = f"https://open.spotify.com/show/{SHOW_ID}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"Error fetching: {e}")
        return None

def extract_episodes_from_html(html):
    """Extract episode IDs and titles from HTML"""
    episodes = []

    # Look for episode links
    episode_pattern = r'/episode/([a-zA-Z0-9]+)'
    matches = re.findall(episode_pattern, html)

    # Get unique episode IDs
    episode_ids = list(dict.fromkeys(matches))

    for ep_id in episode_ids:
        episodes.append({
            'spotify_id': ep_id,
            'spotify_url': f'https://open.spotify.com/episode/{ep_id}'
        })

    return episodes

def match_episodes_by_title(spotify_episodes, local_episodes):
    """Try to match Spotify episodes to local episodes by title similarity"""
    matched = {}

    for local_ep in local_episodes:
        local_title = local_ep.get('title', '').lower()
        local_guest = local_ep.get('guest_name', '').lower()

        for spotify_ep in spotify_episodes:
            # This would need title info from Spotify
            # For now, just store the Spotify URLs we found
            pass

    return matched

def main():
    print("Fetching Spotify episode URLs...")

    # Load local episodes
    with open(EPISODES_FILE) as f:
        data = json.load(f)
        local_episodes = data.get('episodes', [])

    print(f"Local episodes: {len(local_episodes)}")

    # Fetch from Spotify
    html = fetch_spotify_page()
    if html:
        spotify_episodes = extract_episodes_from_html(html)
        print(f"Found {len(spotify_episodes)} Spotify episode IDs")

        # Save what we found
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(spotify_episodes, f, indent=2)

        print(f"Saved to {OUTPUT_FILE}")

        # Print first 10
        print("\nFirst 10 episodes:")
        for ep in spotify_episodes[:10]:
            print(f"  {ep['spotify_url']}")
    else:
        print("Failed to fetch Spotify page")

if __name__ == "__main__":
    main()
