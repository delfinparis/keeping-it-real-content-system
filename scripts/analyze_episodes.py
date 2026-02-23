#!/usr/bin/env python3
"""
Episode Analysis Script for Keeping It Real Podcast
Extracts problems, solutions, clip-worthy moments, and generates video scripts
using AI (OpenAI GPT or Anthropic Claude)
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
import re

# Check for API availability
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
ANALYSIS_DIR = DATA_DIR / "analysis"
CONTENT_DIR = PROJECT_ROOT / "content"
CLIPS_DIR = CONTENT_DIR / "clips"
SCRIPTS_DIR = CONTENT_DIR / "scripts"
PROBLEM_MAP_DIR = CONTENT_DIR / "problem-map"
AVATARS_DIR = CONTENT_DIR / "avatars"
INDEX_DIR = DATA_DIR / "index"

# Ensure directories exist
for dir_path in [ANALYSIS_DIR, CLIPS_DIR, SCRIPTS_DIR, PROBLEM_MAP_DIR, AVATARS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Agent Avatar Profiles
AVATARS = {
    "overwhelmed_newbie": {
        "name": "The Overwhelmed Newbie",
        "experience": "0-2 years, 0-5 deals",
        "challenges": [
            "Just got licensed, doesn't know where to start",
            "No sphere of influence or it's tapped out",
            "Afraid to pick up the phone",
            "Doesn't understand the transaction process",
            "Imposter syndrome",
            "Burning through savings waiting for first deal"
        ]
    },
    "stuck_intermediate": {
        "name": "The Stuck Intermediate",
        "experience": "2-5 years, 6-15 deals",
        "challenges": [
            "Knows enough to be dangerous but not enough to scale",
            "Inconsistent production (feast or famine)",
            "No systems, everything is manual",
            "Working too many hours for too little return",
            "Can't figure out lead generation that works",
            "Considering quitting"
        ]
    },
    "forgotten_middle": {
        "name": "The Forgotten Middle",
        "experience": "5-10 years, 12-24 deals",
        "challenges": [
            "Decent production but plateaued",
            "Not getting attention from brokerage leadership",
            "Missing out on tech/AI revolution",
            "Tired of the hamster wheel",
            "Wants mentorship but too experienced for newbie training",
            "Knows they should do more but lacks accountability"
        ]
    },
    "aspiring_top_producer": {
        "name": "The Aspiring Top Producer",
        "experience": "Any tenure, 25-50 deals",
        "challenges": [
            "Ready to break through to the next level",
            "Needs systems and leverage",
            "Considering building a team",
            "Wants coaching/mastermind community",
            "Looking for edge in competitive market",
            "Hungry but needs direction"
        ]
    },
    "burned_out_veteran": {
        "name": "The Burned-Out Veteran",
        "experience": "10+ years, variable production",
        "challenges": [
            "Has seen every market cycle",
            "Exhausted by constant change",
            "Clients expect 24/7 availability",
            "Technology feels overwhelming",
            "Considering leaving the business",
            "Needs to rediscover why they started"
        ]
    },
    "team_leader": {
        "name": "The Team Leader/Aspiring Team Leader",
        "experience": "Various",
        "challenges": [
            "Wants to scale beyond solo production",
            "Hiring/firing/managing people challenges",
            "Compensation structure questions",
            "Lead distribution problems",
            "Culture and retention issues"
        ]
    }
}

# Problem Categories
PROBLEM_CATEGORIES = {
    "lead_generation": [
        "Where do I find leads?",
        "My sphere is tapped out",
        "I hate cold calling",
        "Online leads don't convert",
        "Open houses don't work",
        "I can't afford paid advertising",
        "Geographic farming isn't working",
        "How do I get more referrals?",
        "FSBO/Expired strategies",
        "Social media isn't generating business",
        "I don't know how to follow up"
    ],
    "conversion_sales": [
        "I have leads but can't convert them",
        "Buyers won't commit / always looking",
        "Sellers won't price correctly",
        "I lose listings to other agents",
        "I don't know what to say at listing appointments",
        "Handling objections",
        "Negotiation skills",
        "Scripts feel inauthentic",
        "Closing techniques",
        "Building rapport with strangers"
    ],
    "time_productivity": [
        "I work 60+ hours and still struggle",
        "No work-life balance",
        "I'm always reactive, never proactive",
        "Can't say no to clients",
        "Shiny object syndrome",
        "No morning routine",
        "Calendar is chaos",
        "I procrastinate on income-producing activities"
    ],
    "systems_operations": [
        "No CRM or don't use mine properly",
        "Transaction coordination overwhelm",
        "No standard operating procedures",
        "Marketing is inconsistent",
        "Database management",
        "Technology stack confusion",
        "Automation — where to start?"
    ],
    "mindset_motivation": [
        "Fear of rejection",
        "Imposter syndrome",
        "Comparison to other agents",
        "Seasonal depression (slow months)",
        "Confidence issues",
        "Burnout",
        "Why am I doing this?",
        "Goal setting that works",
        "Accountability",
        "Handling failure/rejection"
    ],
    "money_business": [
        "Inconsistent income",
        "Don't understand my numbers",
        "Should I join a team?",
        "Commission splits matter",
        "When to hire help",
        "Budgeting for marketing",
        "Taxes and expenses",
        "Building wealth as an agent"
    ],
    "market_industry": [
        "Navigating shifting markets",
        "Interest rate conversations with clients",
        "Inventory shortage strategies",
        "Buyer representation changes (NAR settlement)",
        "How to explain my value",
        "Competing with discount brokerages",
        "What's happening with commissions?"
    ],
    "personal_brand": [
        "I don't know my niche",
        "Social media overwhelm",
        "What content should I create?",
        "Video — I hate being on camera",
        "Personal brand vs. brokerage brand",
        "Building a reputation",
        "Becoming the neighborhood expert"
    ],
    "client_management": [
        "Difficult clients",
        "Setting boundaries",
        "Managing expectations",
        "Ghosting / non-responsive clients",
        "Clients who won't listen to advice",
        "Staying in touch with past clients"
    ]
}

ANALYSIS_PROMPT = """You are analyzing a real estate podcast episode transcript for D.J. Paris, VP of Business Development at Kale Realty. Your goal is to extract actionable insights that can be used for agent recruitment and content creation.

EPISODE INFO:
- File: {filename}
- Guest: {guest_name}
- Duration: {duration}

TRANSCRIPT:
{transcript}

---

Please analyze this transcript and provide a JSON response with the following structure:

{{
  "guest_info": {{
    "name": "<guest full name>",
    "title": "<their title/role if mentioned>",
    "company": "<their company if mentioned>",
    "production_level": "<their production level if mentioned, e.g., 'top 1%', '$10M+ producer'>",
    "specialty": "<their niche or specialty if mentioned>",
    "location": "<their market/location if mentioned>"
  }},

  "main_topics": ["<list of 3-5 main topics covered>"],

  "problems_addressed": [
    {{
      "category": "<one of: lead_generation, conversion_sales, time_productivity, systems_operations, mindset_motivation, money_business, market_industry, personal_brand, client_management>",
      "specific_problem": "<the specific problem discussed>",
      "solution_summary": "<brief summary of the solution or advice given>",
      "timestamp": "<approximate timestamp where this is discussed, e.g., '12:30'>"
    }}
  ],

  "target_avatars": [
    {{
      "avatar_id": "<one of: overwhelmed_newbie, stuck_intermediate, forgotten_middle, aspiring_top_producer, burned_out_veteran, team_leader>",
      "relevance": "<why this episode is relevant to this avatar>",
      "key_takeaway": "<the most important thing this avatar should learn from this episode>"
    }}
  ],

  "clip_worthy_moments": [
    {{
      "timestamp": "<timestamp, e.g., '15:45'>",
      "end_timestamp": "<end timestamp, e.g., '16:30'>",
      "quote": "<the actual quote or key phrase>",
      "clip_type": "<one of: tactical_specificity, contrarian_take, emotional_resonance, memorable_oneliner, pattern_reveal, surprising_statistic, permission_slip, mindset_shift>",
      "why_clipworthy": "<why this would make a good 60-second video>",
      "suggested_hook": "<a hook sentence to start the video>"
    }}
  ],

  "key_tactics": [
    {{
      "tactic": "<specific actionable tactic>",
      "context": "<when/how to apply it>",
      "timestamp": "<where in the episode>"
    }}
  ],

  "quotable_insights": [
    "<memorable quotes that could be used in marketing>"
  ],

  "resources_mentioned": [
    {{
      "type": "<book, tool, website, course, etc.>",
      "name": "<name of resource>",
      "context": "<why it was recommended>"
    }}
  ],

  "episode_summary": "<2-3 sentence summary of the episode's main value proposition>"
}}

Focus on extracting ACTIONABLE, SPECIFIC insights. Avoid generic advice. Look for:
- Specific numbers, scripts, or processes
- Contrarian views that challenge conventional wisdom
- Personal stories with lessons learned
- Tactical tips that can be implemented immediately

Return ONLY valid JSON, no additional text."""


VIDEO_SCRIPT_PROMPT = """You are an expert short-form video script writer for D.J. Paris, VP of Business Development at Kale Realty and host of Keeping It Real Podcast (700+ episodes, 3.2M+ downloads).

Based on this clip-worthy moment from a real estate podcast episode, create a 60-90 second video script.

CLIP INFO:
- Quote/Moment: {quote}
- Type: {clip_type}
- Context: {why_clipworthy}
- Suggested Hook: {suggested_hook}
- Guest: {guest_name}
- Episode Topic: {episode_topic}

---

MANDATORY STRUCTURE (in this exact order — do not reorder):

**HOOK (0:00–0:08)**
The FIRST words out of D.J.'s mouth. No name, no setup. A pattern interrupt — surprising statement, bold claim, or question that stops the scroll. Under 15 words. Opens a curiosity gap the rest of the video must close.

**BRAND INTRO (0:08–0:12)**
Exactly this line, said quickly and naturally: "This is D.J. Paris with Keeping It Real Podcast, and this is your agent tip of the day."

**SETUP (0:12–0:22)**
Context — who said this, where it came from, why it matters. Create a "mirror moment": describe the viewer's specific situation so precisely they think "that's me." Name the pain. Do NOT give the solution yet.

**INSIGHT (0:22–0:45)**
The actual advice, tactic, or story from the guest. Be specific and tactical. Use the guest's real words where possible. Add [ON-SCREEN: key phrase or stat] markers at every key beat for muted viewers. If there's a contrast, use it: "Most agents do X. Top producers do Y."

**REFRAME/APPLICATION (0:45–0:55)**
Why this matters right now. How to apply it this week. "You can do this today." Include a credibility signal where natural (e.g., "This agent closed 47 deals last year using exactly this approach").

**CTA (0:55–1:00+)**
One specific question that invites a comment. Make it easy and direct — not open-ended. Example: "Are you doing this already — yes or no?" or "Which part hits closest to home — drop it below."

**CLOSE**
Exactly this line: "See you next time."

---

ENGAGEMENT PRINCIPLES — apply all of these:

1. CURIOSITY GAP — The hook opens a loop. Don't close it until INSIGHT. The viewer must keep watching to get the answer.
2. 15-SECOND RE-HOOK — At the end of SETUP, add a line that re-engages anyone who almost swiped away. Example: "But here's the part nobody talks about..."
3. MIRROR MOMENT — Recreate the viewer's exact frustration. "You're reaching out to your database but nobody's responding" hits harder than "agents struggle with follow-up."
4. CONTRAST STRUCTURE — Use "Most agents do X. Top producers do Y." wherever it fits naturally.
5. HYPER-SPECIFIC NUMBERS — Vague claims die. Specific numbers live. "3 listings" beats "more listings." "$47,000" beats "significant income."
6. ON-SCREEN TEXT — Add [ON-SCREEN: ...] markers at every key beat. 80%+ of viewers watch on mute.
7. SHAREABLE MOMENT — Engineer one sentence in INSIGHT or REFRAME so quotable a viewer would screenshot it.
8. EMOTIONAL ARC — Guide the viewer: Curious (HOOK) → Seen (SETUP) → Enlightened (INSIGHT) → Motivated (REFRAME) → Engaged (CTA).
9. PACING NOTES — HOOK is punchy, under 12 words. BRAND INTRO is said fast, almost in passing. INSIGHT can breathe and take its time.

---

Also provide:
- CAPTION: A short caption for social media (under 150 characters)
- HASHTAGS: 5 relevant hashtags
- CONTENT_PILLAR: One of [ai_agent, top_producer_secrets, real_talk, market_intelligence, systems_that_scale]
- SHAREABLE_MOMENT: The one sentence from the script most likely to be screenshotted or shared

Return the script in a clean, readable format."""


def load_transcript(transcript_path: Path) -> tuple[str, dict]:
    """Load transcript text and metadata."""
    txt_path = transcript_path.with_suffix('.txt')
    json_path = transcript_path.with_suffix('.json')

    transcript_text = ""
    metadata = {}

    if txt_path.exists():
        with open(txt_path, 'r', encoding='utf-8') as f:
            transcript_text = f.read()

    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

    return transcript_text, metadata


def extract_guest_from_filename(filename: str) -> str:
    """Extract guest name from filename like 2026-01-05_item3_Tim-Burrell.txt"""
    match = re.search(r'_([A-Za-z]+-[A-Za-z]+(?:-[A-Za-z]+)?)', filename)
    if match:
        return match.group(1).replace('-', ' ')
    return "Unknown Guest"


def analyze_with_openai(prompt: str, model: str = "gpt-4o") -> str:
    """Analyze transcript using OpenAI."""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert content analyst specializing in real estate industry podcasts. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    return response.choices[0].message.content


def analyze_with_anthropic(prompt: str, model: str = "claude-sonnet-4-20250514") -> str:
    """Analyze transcript using Anthropic Claude."""
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text


def analyze_episode(transcript_path: Path, provider: str = "anthropic", model: Optional[str] = None) -> dict:
    """Analyze a single episode transcript."""
    transcript_text, metadata = load_transcript(transcript_path)

    if not transcript_text:
        raise ValueError(f"No transcript found for {transcript_path}")

    filename = transcript_path.stem
    guest_name = extract_guest_from_filename(filename)
    duration = metadata.get('duration_formatted', 'Unknown')

    # Truncate transcript if too long (keep first ~80k chars to stay within token limits)
    max_chars = 80000
    if len(transcript_text) > max_chars:
        transcript_text = transcript_text[:max_chars] + "\n\n[TRANSCRIPT TRUNCATED FOR LENGTH]"

    prompt = ANALYSIS_PROMPT.format(
        filename=filename,
        guest_name=guest_name,
        duration=duration,
        transcript=transcript_text
    )

    # Choose provider
    if provider == "openai":
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        model = model or "gpt-4o"
        response = analyze_with_openai(prompt, model)
    else:  # anthropic
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        model = model or "claude-sonnet-4-20250514"
        response = analyze_with_anthropic(prompt, model)

    # Parse JSON response
    try:
        # Clean up response - sometimes LLMs add markdown code blocks
        response = response.strip()
        if response.startswith('```'):
            response = re.sub(r'^```json?\n?', '', response)
            response = re.sub(r'\n?```$', '', response)

        analysis = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse JSON response: {e}")
        print(f"Raw response:\n{response[:500]}...")
        analysis = {"raw_response": response, "parse_error": str(e)}

    # Add metadata
    analysis['_metadata'] = {
        'source_file': filename,
        'analyzed_at': datetime.now().isoformat(),
        'provider': provider,
        'model': model
    }

    return analysis


def generate_video_script(clip: dict, guest_name: str, episode_topic: str, provider: str = "anthropic") -> str:
    """Generate a 60-second video script for a clip-worthy moment."""
    prompt = VIDEO_SCRIPT_PROMPT.format(
        quote=clip.get('quote', ''),
        clip_type=clip.get('clip_type', ''),
        why_clipworthy=clip.get('why_clipworthy', ''),
        suggested_hook=clip.get('suggested_hook', ''),
        guest_name=guest_name,
        episode_topic=episode_topic
    )

    if provider == "openai":
        return analyze_with_openai(prompt, "gpt-4o")
    else:
        return analyze_with_anthropic(prompt)


def save_analysis(analysis: dict, filename: str):
    """Save analysis results to appropriate locations."""
    base_name = Path(filename).stem

    # Save full analysis
    analysis_path = ANALYSIS_DIR / f"{base_name}_analysis.json"
    with open(analysis_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"  Saved analysis to {analysis_path}")

    # Save clips
    if 'clip_worthy_moments' in analysis and analysis['clip_worthy_moments']:
        clips_path = CLIPS_DIR / f"{base_name}_clips.json"
        with open(clips_path, 'w', encoding='utf-8') as f:
            json.dump(analysis['clip_worthy_moments'], f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(analysis['clip_worthy_moments'])} clips to {clips_path}")

    return analysis_path


def update_problem_map(analysis: dict, filename: str):
    """Update the problem-to-episode mapping."""
    problem_map_path = PROBLEM_MAP_DIR / "problem_episode_map.json"

    # Load existing map or create new
    if problem_map_path.exists():
        with open(problem_map_path, 'r', encoding='utf-8') as f:
            problem_map = json.load(f)
    else:
        problem_map = {cat: {} for cat in PROBLEM_CATEGORIES.keys()}

    base_name = Path(filename).stem

    # Add this episode to relevant problems
    for problem in analysis.get('problems_addressed', []):
        category = problem.get('category', 'uncategorized')
        specific = problem.get('specific_problem', 'general')

        if category not in problem_map:
            problem_map[category] = {}

        if specific not in problem_map[category]:
            problem_map[category][specific] = []

        if base_name not in problem_map[category][specific]:
            problem_map[category][specific].append({
                'episode': base_name,
                'solution_summary': problem.get('solution_summary', ''),
                'timestamp': problem.get('timestamp', '')
            })

    # Save updated map
    with open(problem_map_path, 'w', encoding='utf-8') as f:
        json.dump(problem_map, f, indent=2, ensure_ascii=False)
    print(f"  Updated problem map at {problem_map_path}")


def update_avatar_map(analysis: dict, filename: str):
    """Update the avatar-to-episode mapping."""
    avatar_map_path = AVATARS_DIR / "avatar_episode_map.json"

    # Load existing map or create new
    if avatar_map_path.exists():
        with open(avatar_map_path, 'r', encoding='utf-8') as f:
            avatar_map = json.load(f)
    else:
        avatar_map = {avatar_id: [] for avatar_id in AVATARS.keys()}

    base_name = Path(filename).stem

    # Add this episode to relevant avatars
    for avatar in analysis.get('target_avatars', []):
        avatar_id = avatar.get('avatar_id', 'unknown')

        if avatar_id not in avatar_map:
            avatar_map[avatar_id] = []

        # Check if already added
        existing = [e for e in avatar_map[avatar_id] if e.get('episode') == base_name]
        if not existing:
            avatar_map[avatar_id].append({
                'episode': base_name,
                'relevance': avatar.get('relevance', ''),
                'key_takeaway': avatar.get('key_takeaway', '')
            })

    # Save updated map
    with open(avatar_map_path, 'w', encoding='utf-8') as f:
        json.dump(avatar_map, f, indent=2, ensure_ascii=False)
    print(f"  Updated avatar map at {avatar_map_path}")


def update_progress(analyzed_count: int):
    """Update the progress tracker."""
    progress_path = INDEX_DIR / "progress.json"

    if progress_path.exists():
        with open(progress_path, 'r', encoding='utf-8') as f:
            progress = json.load(f)
    else:
        progress = {}

    progress['analyzed'] = analyzed_count
    progress['last_analysis'] = datetime.now().isoformat()

    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


def get_transcripts_to_analyze() -> list[Path]:
    """Get list of transcripts that haven't been analyzed yet."""
    transcripts = list(TRANSCRIPTS_DIR.glob("*.txt"))
    analyzed = set(p.stem.replace('_analysis', '') for p in ANALYSIS_DIR.glob("*_analysis.json"))

    to_analyze = []
    for t in transcripts:
        if t.stem not in analyzed:
            to_analyze.append(t)

    return sorted(to_analyze)


def show_status():
    """Show current analysis status."""
    transcripts = list(TRANSCRIPTS_DIR.glob("*.txt"))
    analyzed = list(ANALYSIS_DIR.glob("*_analysis.json"))
    clips = list(CLIPS_DIR.glob("*.json"))

    print("\n=== Analysis Status ===")
    print(f"Transcripts available: {len(transcripts)}")
    print(f"Episodes analyzed: {len(analyzed)}")
    print(f"Clip files generated: {len(clips)}")

    # Count total clips
    total_clips = 0
    for clip_file in clips:
        with open(clip_file, 'r') as f:
            clip_data = json.load(f)
            total_clips += len(clip_data)
    print(f"Total clip-worthy moments: {total_clips}")

    # Check mappings
    problem_map_path = PROBLEM_MAP_DIR / "problem_episode_map.json"
    avatar_map_path = AVATARS_DIR / "avatar_episode_map.json"

    if problem_map_path.exists():
        with open(problem_map_path, 'r') as f:
            pm = json.load(f)
            total_problems = sum(len(problems) for problems in pm.values())
            print(f"Problems mapped: {total_problems}")

    if avatar_map_path.exists():
        with open(avatar_map_path, 'r') as f:
            am = json.load(f)
            for avatar_id, episodes in am.items():
                if episodes:
                    print(f"  {AVATARS.get(avatar_id, {}).get('name', avatar_id)}: {len(episodes)} episodes")

    # Show pending
    pending = get_transcripts_to_analyze()
    if pending:
        print(f"\nPending analysis: {len(pending)} episodes")
        for p in pending[:5]:
            print(f"  - {p.stem}")
        if len(pending) > 5:
            print(f"  ... and {len(pending) - 5} more")


def main():
    parser = argparse.ArgumentParser(description='Analyze podcast episode transcripts')
    parser.add_argument('--status', action='store_true', help='Show analysis status')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of episodes to analyze')
    parser.add_argument('--episode', type=str, help='Analyze a specific episode (filename without extension)')
    parser.add_argument('--provider', choices=['openai', 'anthropic'], default='anthropic',
                        help='AI provider to use (default: anthropic)')
    parser.add_argument('--model', type=str, help='Specific model to use')
    parser.add_argument('--generate-scripts', action='store_true',
                        help='Also generate video scripts for clips')

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    # Get episodes to analyze
    if args.episode:
        transcript_path = TRANSCRIPTS_DIR / f"{args.episode}.txt"
        if not transcript_path.exists():
            print(f"Error: Transcript not found: {transcript_path}")
            return
        episodes = [transcript_path]
    else:
        episodes = get_transcripts_to_analyze()
        if args.limit > 0:
            episodes = episodes[:args.limit]

    if not episodes:
        print("No episodes to analyze. All transcripts have been processed.")
        show_status()
        return

    print(f"\nAnalyzing {len(episodes)} episode(s) using {args.provider}...")

    analyzed_count = len(list(ANALYSIS_DIR.glob("*_analysis.json")))

    for i, transcript_path in enumerate(episodes, 1):
        print(f"\n[{i}/{len(episodes)}] Analyzing: {transcript_path.stem}")

        try:
            # Analyze episode
            analysis = analyze_episode(transcript_path, provider=args.provider, model=args.model)

            # Save results
            save_analysis(analysis, transcript_path.name)

            # Update mappings
            if 'problems_addressed' in analysis:
                update_problem_map(analysis, transcript_path.name)

            if 'target_avatars' in analysis:
                update_avatar_map(analysis, transcript_path.name)

            # Generate video scripts if requested
            if args.generate_scripts and 'clip_worthy_moments' in analysis:
                guest_name = analysis.get('guest_info', {}).get('name', 'Unknown')
                episode_topic = ', '.join(analysis.get('main_topics', ['Real Estate']))

                scripts = []
                for clip in analysis['clip_worthy_moments'][:3]:  # Top 3 clips
                    print(f"    Generating script for clip: {clip.get('timestamp', 'N/A')}")
                    script = generate_video_script(clip, guest_name, episode_topic, args.provider)
                    scripts.append({
                        'clip': clip,
                        'script': script
                    })

                # Save scripts
                scripts_path = SCRIPTS_DIR / f"{transcript_path.stem}_scripts.json"
                with open(scripts_path, 'w', encoding='utf-8') as f:
                    json.dump(scripts, f, indent=2, ensure_ascii=False)
                print(f"  Saved {len(scripts)} video scripts to {scripts_path}")

            analyzed_count += 1

        except Exception as e:
            print(f"  Error analyzing {transcript_path.stem}: {e}")
            continue

    # Update progress
    update_progress(analyzed_count)

    print("\n" + "="*50)
    show_status()


if __name__ == "__main__":
    main()
