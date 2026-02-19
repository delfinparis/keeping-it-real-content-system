# Prompt System: Social Media Video Scripts from Podcast Episodes

A 5-stage prompt pipeline for mining podcast transcripts, writing high-performing 60-second video scripts, and sequencing them into a content calendar.

---

## The Pipeline

```
TRANSCRIPT → [01 Clip Hunter] → [02 Script Writer] → [03 Platform Adapter] → PUBLISH
                                        ↓                      ↓
                                  [04 Kill Judge] ←────────────┘
                                        ↓
                                  REWRITE or KILL
                                        ↓
                              [05 Content Sequencer] → CALENDAR
```

| Stage | Prompt | Input | Output |
|-------|--------|-------|--------|
| 1 | [01_clip_hunter.md](01_clip_hunter.md) | Raw transcript | 2-4 clip-worthy moments with timestamps, quotes, hooks |
| 2 | [02_script_writer.md](02_script_writer.md) | Clip data from Stage 1 | Full 60-second script with production notes |
| 3 | [03_platform_adapter.md](03_platform_adapter.md) | Base script from Stage 2 | TikTok, Instagram, YouTube Shorts, LinkedIn versions |
| 4 | [04_kill_judge.md](04_kill_judge.md) | Scripts from Stage 2 or 3 | Scored reviews: PUBLISH / REWRITE / KILL |
| 5 | [05_content_sequencer.md](05_content_sequencer.md) | Approved scripts (score 7+) | Weekly content calendar with rationale |

---

## Roles (8 + 2 Meta)

Each prompt activates specific expert roles. Roles are sharp and non-overlapping.

| # | Role | Appears In | Mandate |
|---|------|-----------|---------|
| 1 | Clip Hunter | Prompt 01 | Find the moment the guest said something they've never said before |
| 2 | Scroll-Stop Architect | Prompt 02 | The first 3 seconds must create an open loop the viewer cannot leave |
| 3 | Guest Voice Guardian | Prompt 02 | The script must sound like *them*, not like a marketer writing about them |
| 4 | 60-Second Dramaturg | Prompt 02 | Every second earns the next — pacing, beats, silence, the turn |
| 5 | Agent Whisperer | Prompt 02 | Speaks directly to a specific avatar's pain, not "agents in general" |
| 6 | Platform Native | Prompt 03 | Writes differently for TikTok vs. Reels vs. Shorts vs. LinkedIn |
| 7 | Production-Aware Writer | Prompt 03 | Scripts include visual cues, text overlay moments, and b-roll notes |
| 8 | CTA Engineer | Prompt 03 | The last 8 seconds create a follower, not just a viewer |
| **M1** | Kill Judge | Prompt 04 | Scores every script 1-10, kills anything below 4, rewrites 4-6 |
| **M2** | Content Sequencer | Prompt 05 | Ensures weekly output has variety, rhythm, and avatar coverage |

---

## Key Concepts Embedded in Every Prompt

### The Viewer Is Always Present
Every prompt includes the target viewer as a primary constraint. Not "real estate agents" — a *specific person* with a specific struggle, scrolling at a specific time.

### 6 Agent Avatars
| Avatar | Experience | Production | Core Pain |
|--------|-----------|------------|-----------|
| Overwhelmed Newbie | 0-2 years | 0-5 deals | "Where do I even start?" |
| Stuck Intermediate | 2-5 years | 6-15 deals | "Why isn't this working?" |
| Forgotten Middle | 5-10 years | 12-24 deals | "I'm invisible and plateaued" |
| Aspiring Top Producer | Any tenure | 25-50 deals | "How do I break through?" |
| Burned-Out Veteran | 10+ years | Variable | "I can't keep doing this" |
| Team Leader | Various | Various | "People are harder than deals" |

### 5 Content Pillars
1. **The AI Agent** — AI tools and tactics for real estate
2. **Top Producer Secrets** — Tactics from $10M+ producers
3. **Real Talk** — Emotional/mindset content, permission slips
4. **Market Intelligence** — Market commentary, client conversation scripts
5. **Systems That Scale** — Productivity, tech stack, time management

### 8 Clip Types
tactical_specificity | contrarian_take | emotional_resonance | memorable_oneliner | pattern_reveal | surprising_statistic | permission_slip | mindset_shift

---

## How to Use

### Full Pipeline (New Transcript)
```
1. Feed transcript → Prompt 01 (Clip Hunter)
2. Feed each clip → Prompt 02 (Script Writer)
3. Feed each script → Prompt 04 (Kill Judge)
4. Scripts scoring 7+ → Prompt 03 (Platform Adapter)
5. All approved scripts → Prompt 05 (Content Sequencer)
```

### Quick Script (Already Have a Clip)
```
1. Feed clip data → Prompt 02 (Script Writer)
2. Feed script → Prompt 04 (Kill Judge)
3. If approved → Prompt 03 (Platform Adapter)
```

### Quality Check Existing Scripts
```
1. Feed existing scripts → Prompt 04 (Kill Judge)
2. Rewrite flagged scripts using Prompt 02 with Kill Judge's notes
```

### Plan Next Week's Content
```
1. Gather all approved scripts → Prompt 05 (Content Sequencer)
```

---

## Upgrading the Existing Python Pipeline

The current `scripts/analyze_episodes.py` uses two prompts:
- `ANALYSIS_PROMPT` — general analysis (maps to Prompt 01, but broader)
- `VIDEO_SCRIPT_PROMPT` — script generation (maps to Prompt 02, but weaker)

To integrate this prompt system:
1. Replace `VIDEO_SCRIPT_PROMPT` with Prompt 02's user prompt
2. Add Prompt 04 as a post-processing quality gate
3. Add Prompt 03 for platform-specific versions
4. Add Prompt 05 for calendar planning (separate script or notebook)

The `ANALYSIS_PROMPT` can remain for extracting problems, avatars, and episode metadata. Prompt 01 specifically replaces and upgrades the `clip_worthy_moments` extraction.

---

## What Makes This System Different from Generic Prompting

1. **Few-shot examples with BEFORE/AFTER** — Each prompt shows what bad output looks like and why, alongside upgraded output. This anchors quality.

2. **The viewer is a constraint, not an afterthought** — Every prompt names the specific person watching and their emotional state.

3. **Anti-patterns are explicit** — Each prompt lists what NOT to do (e.g., "Never start with 'Meet [Guest Name]'"), preventing the most common failure modes.

4. **Production awareness** — Scripts include visual/audio direction, not just words. This bridges the gap between writer and video editor.

5. **Quality gate built into the pipeline** — The Kill Judge prevents mediocre scripts from reaching the calendar. Most content systems skip this step.

6. **Guest voice preservation** — The Voice Guardian role ensures scripts sound like the guest, not like a content agency.

---

*Created: 2026-02-19*
*For: Keeping It Real Podcast / Kale Realty content system*
