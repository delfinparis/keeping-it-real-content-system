#!/usr/bin/env python3
"""
Script Generator V2 — Uses upgraded prompt system
Generates 60-second video scripts from existing clip data + transcripts
using the new role-based prompt architecture.
"""

import os
import json
import re
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
ANALYSIS_DIR = DATA_DIR / "analysis"
CONTENT_DIR = PROJECT_ROOT / "content"
CLIPS_DIR = CONTENT_DIR / "clips"
SCRIPTS_DIR = CONTENT_DIR / "scripts"

SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# PROMPT: Combined Clip Enhancement + Script Writer (Prompt 01 + 02 merged)
# This runs in a single API call per clip for efficiency.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are two experts working in sequence:

FIRST — You are a CLIP HUNTER: an investigative journalist with an ear for the moment a guest says something they've never said publicly before. You assess the raw clip data, the surrounding transcript, and determine the guest's voice profile, energy, and the sharpest possible hook.

THEN — You are a 60-SECOND DRAMATURG: a short-form video scriptwriter with thousands of scripts and hundreds of millions of views. You write scripts where every second earns the next second.

Your rules:

1. THE 3-SECOND RULE: If the first sentence doesn't create a genuine "wait, what?" reaction, start over. No "Meet [name]." No "Did you know...?" No "In today's video." The hook must be a provocation, a contradiction, or an impossible-sounding fact.

2. THE VOICE RULE: The script must sound like it was written to be SPOKEN, not read. Contractions. Fragments. The rhythm of actual speech. If it sounds like a LinkedIn post, rewrite it.

3. THE GUEST RULE: Honor the guest's actual words and voice. If they speak in metaphors, use metaphors. If they're data-driven, lead with numbers. If they're blunt, be blunt. Do not sanitize personality into corporate smoothness.

4. THE ONE-VIEWER RULE: You are writing for ONE specific person — the target avatar. Write as if speaking directly to them about their specific struggle.

5. THE EARN-IT RULE: Every section earns the next. HOOK earns SETUP. SETUP earns INSIGHT. INSIGHT earns REFRAME. REFRAME earns CTA. Dead weight gets cut.

6. THE PRODUCTION RULE: Include visual/production notes. This script will be filmed or edited over footage.

Return ONLY valid JSON. No markdown code blocks. No additional text."""


def build_user_prompt(clip, guest_info, main_topics, episode_summary, transcript_excerpt):
    """Build the combined clip enhancement + script writer prompt."""

    guest_name = guest_info.get("name", "Unknown Guest")
    credibility = guest_info.get("production_level", "")
    if not credibility:
        credibility = guest_info.get("title", "")
    specialty = guest_info.get("specialty", "")
    location = guest_info.get("location", "")

    guest_context = f"{guest_name}"
    if credibility:
        guest_context += f" — {credibility}"
    if specialty:
        guest_context += f", {specialty}"
    if location:
        guest_context += f" ({location})"

    topics_str = ", ".join(main_topics) if main_topics else "Real Estate"

    return f"""CLIP DATA:
- Guest: {guest_context}
- Verbatim Quote: "{clip.get('quote', '')}"
- Timestamp: {clip.get('timestamp', 'N/A')} - {clip.get('end_timestamp', 'N/A')}
- Clip Type: {clip.get('clip_type', 'unknown')}
- Initial Assessment: {clip.get('why_clipworthy', '')}
- Initial Hook Idea: {clip.get('suggested_hook', '')}

EPISODE CONTEXT:
- Topics: {topics_str}
- Summary: {episode_summary}

TRANSCRIPT EXCERPT (around the clip timestamp, for voice and context):
{transcript_excerpt}

---

STEP 1: Assess this clip and determine:
- The guest's speaking style from the transcript excerpt
- The energy/tone of the moment (passionate, reflective, matter-of-fact, emotional, humorous)
- Which agent avatar this hits hardest (one of: overwhelmed_newbie, stuck_intermediate, forgotten_middle, aspiring_top_producer, burned_out_veteran, team_leader)
- A scroll-stopping hook that is NOT a question format and does NOT start with "Meet [name]"

STEP 2: Write the 60-second script.

Return as a single JSON object:

{{
  "clip_assessment": {{
    "verbatim_quote": "<the guest's exact words — preserve their language>",
    "clip_type": "<clip type>",
    "energy": "<high_passionate | calm_authoritative | reflective_vulnerable | matter_of_fact | humorous_irreverent>",
    "guest_voice": "<1-2 sentence description of how this guest talks>",
    "target_avatar": "<avatar_id>",
    "why_this_stops_scrolls": "<1 sentence — what makes this worth 60 seconds of someone's life?>"
  }},
  "script": {{
    "HOOK": {{
      "timing": "0:00-0:03",
      "text": "<The scroll-stopper. 1-2 sentences max. Must create an open loop or identity threat. No introductions.>",
      "production_note": "<Visual direction>"
    }},
    "SETUP": {{
      "timing": "0:03-0:12",
      "text": "<Why should the target avatar care? Connect to THEIR reality. Introduce guest through credibility marker only.>",
      "production_note": "<Visual direction>"
    }},
    "INSIGHT": {{
      "timing": "0:12-0:38",
      "text": "<The substance. Weave in the guest's actual quote. Be specific — numbers, steps, scripts, tactics.>",
      "production_note": "<Visual direction>"
    }},
    "REFRAME": {{
      "timing": "0:38-0:50",
      "text": "<The 'so what' — personal to the target avatar. Paint what changes for THEM.>",
      "production_note": "<Visual direction>"
    }},
    "CTA": {{
      "timing": "0:50-0:60",
      "text": "<Specific action they can take TODAY, or a question that haunts them. Not 'follow for more.'>",
      "production_note": "<Visual direction>"
    }}
  }},
  "caption": "<Under 150 chars. Like a text to a friend, not a press release.>",
  "hashtags": ["<5 hashtags — mix reach and niche>"],
  "content_pillar": "<one of: ai_agent, top_producer_secrets, real_talk, market_intelligence, systems_that_scale>",
  "target_avatar": "<avatar_id>",
  "share_trigger": "<identity | utility | debate — why would someone share this?>"
}}"""


def parse_timestamp_to_seconds(ts):
    """Convert timestamp string to seconds. Handles HH:MM:SS, MM:SS, and seconds."""
    if not ts:
        return 0
    ts = ts.strip()
    # Remove brackets if present
    ts = ts.strip("[]")
    parts = ts.split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return int(float(parts[0]))
    except (ValueError, IndexError):
        return 0


def extract_transcript_excerpt(transcript_text, timestamp, window_seconds=180):
    """Extract a section of transcript around a given timestamp."""
    if not transcript_text:
        return "[No transcript available]"

    target_seconds = parse_timestamp_to_seconds(timestamp)

    # Parse transcript lines with timestamps
    lines = transcript_text.split("\n")
    timestamped_lines = []

    for line in lines:
        match = re.match(r'\[(\d{2}:\d{2}:\d{2})\]\s*(.*)', line)
        if match:
            line_seconds = parse_timestamp_to_seconds(match.group(1))
            timestamped_lines.append((line_seconds, line))
        else:
            # Non-timestamped lines get attached to previous timestamp
            if timestamped_lines:
                prev_sec, prev_text = timestamped_lines[-1]
                timestamped_lines[-1] = (prev_sec, prev_text + " " + line.strip())

    if not timestamped_lines:
        # No timestamps found — return a chunk from the middle
        total_chars = len(transcript_text)
        midpoint = total_chars // 3  # roughly where the good stuff is
        return transcript_text[midpoint:midpoint + 3000]

    # Find lines within window around the target timestamp
    start = max(0, target_seconds - window_seconds)
    end = target_seconds + window_seconds

    excerpt_lines = [text for sec, text in timestamped_lines if start <= sec <= end]

    if not excerpt_lines:
        # Fallback: return lines closest to target
        sorted_by_distance = sorted(timestamped_lines, key=lambda x: abs(x[0] - target_seconds))
        excerpt_lines = [text for _, text in sorted_by_distance[:30]]

    excerpt = "\n".join(excerpt_lines)

    # Cap at ~3000 chars to keep within token limits
    if len(excerpt) > 3000:
        excerpt = excerpt[:3000] + "\n[...excerpt truncated...]"

    return excerpt


def load_episode_data(clip_filename):
    """Load all available data for an episode from its clip filename."""
    # Extract base name: e.g., "2026-01-22_item1_Kristee-Leonard" from clips filename
    base = clip_filename.replace("_clips.json", "")

    # Load clip data
    clip_path = CLIPS_DIR / clip_filename
    with open(clip_path, "r", encoding="utf-8") as f:
        clips = json.load(f)

    # Load analysis data
    analysis_path = ANALYSIS_DIR / f"{base}_analysis.json"
    analysis = {}
    if analysis_path.exists():
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis = json.load(f)

    # Load transcript
    transcript_path = TRANSCRIPTS_DIR / f"{base}.txt"
    transcript_text = ""
    if transcript_path.exists():
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_text = f.read()

    guest_info = analysis.get("guest_info", {})
    if not guest_info.get("name"):
        # Extract from filename
        name_match = re.search(r'_([A-Za-z]+-[A-Za-z]+(?:-[A-Za-z]+)?)', base)
        if name_match:
            guest_info["name"] = name_match.group(1).replace("-", " ")

    return {
        "base_name": base,
        "clips": clips,
        "guest_info": guest_info,
        "main_topics": analysis.get("main_topics", []),
        "episode_summary": analysis.get("episode_summary", ""),
        "transcript_text": transcript_text,
    }


def generate_script(client, clip, episode_data, model="claude-sonnet-4-5-20250929"):
    """Generate a single script for a clip using the Anthropic API."""
    transcript_excerpt = extract_transcript_excerpt(
        episode_data["transcript_text"],
        clip.get("timestamp", ""),
    )

    user_prompt = build_user_prompt(
        clip=clip,
        guest_info=episode_data["guest_info"],
        main_topics=episode_data["main_topics"],
        episode_summary=episode_data["episode_summary"],
        transcript_excerpt=transcript_excerpt,
    )

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[{"role": "user", "content": user_prompt}],
        system=SYSTEM_PROMPT,
        temperature=0.7,
    )

    raw = response.content[0].text.strip()

    # Clean markdown code blocks if present
    if raw.startswith("```"):
        raw = re.sub(r'^```json?\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)

    try:
        script_data = json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract JSON from the response
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            try:
                script_data = json.loads(json_match.group())
            except json.JSONDecodeError:
                script_data = {"raw_response": raw, "parse_error": True}
        else:
            script_data = {"raw_response": raw, "parse_error": True}

    # Add metadata
    script_data["_metadata"] = {
        "source_clip_timestamp": clip.get("timestamp", ""),
        "source_episode": episode_data["base_name"],
        "guest_name": episode_data["guest_info"].get("name", "Unknown"),
        "generated_at": datetime.now().isoformat(),
        "model": model,
        "prompt_version": "v2",
    }

    # Track token usage
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    return script_data, usage


def select_clips_for_generation(target_count=100):
    """Select the best clips across all episodes to generate target_count scripts.

    Strategy:
    - Prioritize episodes with analysis data (richer context)
    - Pick at most 2 clips per episode for variety
    - Prefer recent episodes first
    - Ensure diversity of clip types
    """
    clip_files = sorted(CLIPS_DIR.glob("*.json"), reverse=True)  # newest first

    candidates = []
    for clip_file in clip_files:
        base = clip_file.stem.replace("_clips", "")
        analysis_path = ANALYSIS_DIR / f"{base}_analysis.json"
        transcript_path = TRANSCRIPTS_DIR / f"{base}.txt"

        # Prefer episodes with both analysis AND transcript
        has_analysis = analysis_path.exists()
        has_transcript = transcript_path.exists()

        if not has_transcript:
            continue  # Skip episodes without transcripts — can't get voice context

        with open(clip_file, "r", encoding="utf-8") as f:
            clips = json.load(f)

        # Take up to 2 clips per episode
        for i, clip in enumerate(clips[:2]):
            candidates.append({
                "clip_file": clip_file.name,
                "clip_index": i,
                "clip": clip,
                "has_analysis": has_analysis,
                "has_transcript": has_transcript,
                "priority": (2 if has_analysis else 0) + (1 if has_transcript else 0),
            })

    # Sort by priority (best data first), then by recency (already sorted by filename)
    candidates.sort(key=lambda x: x["priority"], reverse=True)

    # Ensure clip type diversity
    type_counts = {}
    selected = []

    for c in candidates:
        if len(selected) >= target_count:
            break

        clip_type = c["clip"].get("clip_type", "unknown")
        type_counts[clip_type] = type_counts.get(clip_type, 0) + 1

        # Don't let any single clip type dominate (max 30% of total)
        if type_counts[clip_type] > target_count * 0.3:
            continue

        selected.append(c)

    return selected


def main():
    parser = argparse.ArgumentParser(description="Generate V2 video scripts using upgraded prompts")
    parser.add_argument("--count", type=int, default=100, help="Number of scripts to generate (default: 100)")
    parser.add_argument("--model", type=str, default="claude-sonnet-4-5-20250929",
                        help="Anthropic model to use (default: claude-sonnet-4-5-20250929)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without making API calls")
    parser.add_argument("--resume", action="store_true", help="Skip clips that already have scripts")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between API calls in seconds (default: 1.0)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Script Generator V2 — Upgraded Prompt System")
    print(f"{'='*60}")
    print(f"Model: {args.model}")
    print(f"Target: {args.count} scripts")
    print()

    # Select clips
    print("Selecting best clips for script generation...")
    selected = select_clips_for_generation(args.count)
    print(f"Selected {len(selected)} clips from {len(set(c['clip_file'] for c in selected))} episodes")

    # Show clip type distribution
    type_dist = {}
    for c in selected:
        ct = c["clip"].get("clip_type", "unknown")
        type_dist[ct] = type_dist.get(ct, 0) + 1
    print("\nClip type distribution:")
    for ct, count in sorted(type_dist.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")

    if args.dry_run:
        print("\n[DRY RUN] Would generate scripts for:")
        for i, c in enumerate(selected[:20]):
            clip = c["clip"]
            print(f"  {i+1}. {c['clip_file']} — \"{clip.get('quote', '')[:60]}...\"")
        if len(selected) > 20:
            print(f"  ... and {len(selected) - 20} more")

        # Cost estimate
        est_input_tokens = len(selected) * 2500  # ~2500 tokens per call
        est_output_tokens = len(selected) * 1200  # ~1200 tokens per response
        # Sonnet pricing: $3/M input, $15/M output
        est_cost = (est_input_tokens * 3 / 1_000_000) + (est_output_tokens * 15 / 1_000_000)
        print(f"\nEstimated cost: ~${est_cost:.2f}")
        print(f"Estimated time: ~{len(selected) * 4 / 60:.0f} minutes")
        return

    # Check API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set.")
        print("Run: export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    # Initialize client
    client = anthropic.Anthropic()

    # Generate scripts
    total_input_tokens = 0
    total_output_tokens = 0
    generated = 0
    errors = 0
    start_time = time.time()

    # Cache loaded episode data to avoid re-reading files
    episode_cache = {}

    for i, candidate in enumerate(selected):
        clip_file = candidate["clip_file"]
        clip_index = candidate["clip_index"]
        clip = candidate["clip"]

        # Check if script already exists (for resume mode)
        base = clip_file.replace("_clips.json", "")
        script_filename = f"{base}_clip{clip_index}_v2.json"
        script_path = SCRIPTS_DIR / script_filename

        if args.resume and script_path.exists():
            print(f"  [{i+1}/{len(selected)}] SKIP (exists): {script_filename}")
            generated += 1
            continue

        # Load episode data (cached)
        if clip_file not in episode_cache:
            try:
                episode_cache[clip_file] = load_episode_data(clip_file)
            except Exception as e:
                print(f"  [{i+1}/{len(selected)}] ERROR loading {clip_file}: {e}")
                errors += 1
                continue

        episode_data = episode_cache[clip_file]
        guest = episode_data["guest_info"].get("name", "Unknown")
        quote_preview = clip.get("quote", "")[:50]

        print(f"  [{i+1}/{len(selected)}] {guest} — \"{quote_preview}...\"", end="", flush=True)

        try:
            script_data, usage = generate_script(client, clip, episode_data, args.model)

            total_input_tokens += usage["input_tokens"]
            total_output_tokens += usage["output_tokens"]

            # Save script
            with open(script_path, "w", encoding="utf-8") as f:
                json.dump(script_data, f, indent=2, ensure_ascii=False)

            generated += 1
            print(f" ✓ ({usage['input_tokens']}+{usage['output_tokens']} tokens)")

        except anthropic.RateLimitError:
            print(f" RATE LIMITED — waiting 60s...")
            time.sleep(60)
            # Retry once
            try:
                script_data, usage = generate_script(client, clip, episode_data, args.model)
                total_input_tokens += usage["input_tokens"]
                total_output_tokens += usage["output_tokens"]
                with open(script_path, "w", encoding="utf-8") as f:
                    json.dump(script_data, f, indent=2, ensure_ascii=False)
                generated += 1
                print(f" ✓ (retry succeeded)")
            except Exception as e2:
                print(f" ✗ (retry failed: {e2})")
                errors += 1

        except Exception as e:
            print(f" ✗ ({e})")
            errors += 1

        # Rate limiting delay
        if i < len(selected) - 1:
            time.sleep(args.delay)

        # Progress update every 10 scripts
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed * 60
            remaining = (len(selected) - i - 1) / rate if rate > 0 else 0
            print(f"\n  --- Progress: {generated}/{len(selected)} generated, "
                  f"{errors} errors, {rate:.0f}/min, ~{remaining:.0f}min remaining ---\n")

    # Final summary
    elapsed = time.time() - start_time
    est_cost = (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)

    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Scripts generated: {generated}")
    print(f"Errors: {errors}")
    print(f"Total tokens: {total_input_tokens:,} input + {total_output_tokens:,} output")
    print(f"Estimated cost: ${est_cost:.2f}")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"Scripts saved to: {SCRIPTS_DIR}")
    print()

    # List generated files
    new_scripts = sorted(SCRIPTS_DIR.glob("*_v2.json"))
    print(f"Total V2 scripts on disk: {len(new_scripts)}")


if __name__ == "__main__":
    main()
