import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
import episodesData from "@/data/episodes.json";
const episodes = episodesData.episodes;
import allAnalysis from "@/data/all_analysis.json";

interface AnalysisData {
  guest_info?: {
    name?: string | null;
    title?: string | null;
    company?: string | null;
    production_level?: string | null;
    specialty?: string | null;
    location?: string | null;
  };
  main_topics?: string[];
  problems_addressed?: Array<{
    category: string;
    specific_problem: string;
    solution_summary: string;
    timestamp: string;
  }>;
  target_avatars?: Array<{
    avatar_id: string;
    relevance: string;
    key_takeaway: string;
  }>;
  clip_worthy_moments?: Array<{
    timestamp: string;
    end_timestamp: string;
    quote: string;
    clip_type: string;
    why_clipworthy: string;
    suggested_hook: string;
  }>;
  key_tactics?: Array<{
    tactic: string;
    context: string;
    timestamp: string;
  }>;
  quotable_insights?: string[];
  resources_mentioned?: Array<{
    type: string;
    name: string;
    context: string;
  }>;
  episode_summary?: string;
}

const analysisData = allAnalysis as Record<string, AnalysisData>;

// Build a searchable index of problems and keywords
interface SearchIndex {
  byProblem: Map<string, string[]>;
  byKeyword: Map<string, string[]>;
  byCategory: Map<string, string[]>;
}

function buildSearchIndex(): SearchIndex {
  const byProblem = new Map<string, string[]>();
  const byKeyword = new Map<string, string[]>();
  const byCategory = new Map<string, string[]>();

  for (const [episodeId, data] of Object.entries(analysisData)) {
    // Index by problem category
    data.problems_addressed?.forEach((p) => {
      const cat = p.category.toLowerCase();
      if (!byCategory.has(cat)) byCategory.set(cat, []);
      byCategory.get(cat)!.push(episodeId);

      // Index by specific problem keywords
      const words = p.specific_problem.toLowerCase().split(/\s+/);
      words.forEach((word) => {
        if (word.length > 3) {
          if (!byKeyword.has(word)) byKeyword.set(word, []);
          byKeyword.get(word)!.push(episodeId);
        }
      });
    });

    // Index by topics
    data.main_topics?.forEach((topic) => {
      const words = topic.toLowerCase().split(/\s+/);
      words.forEach((word) => {
        if (word.length > 3) {
          if (!byKeyword.has(word)) byKeyword.set(word, []);
          byKeyword.get(word)!.push(episodeId);
        }
      });
    });
  }

  return { byProblem, byKeyword, byCategory };
}

const searchIndex = buildSearchIndex();

// Create a condensed summary for the AI prompt (top 50 most relevant)
function getRelevantEpisodeSummaries(challenge: string, limit = 30): string {
  const keywords = challenge.toLowerCase().split(/\s+/).filter((w) => w.length > 3);
  const scores = new Map<string, number>();

  // Score episodes by keyword matches
  keywords.forEach((kw) => {
    searchIndex.byKeyword.get(kw)?.forEach((epId) => {
      scores.set(epId, (scores.get(epId) || 0) + 2);
    });
  });

  // Boost by category matches
  const categoryKeywords = ["lead", "marketing", "social", "conversion", "mindset", "time", "systems", "brand"];
  keywords.forEach((kw) => {
    categoryKeywords.forEach((cat) => {
      if (kw.includes(cat) || cat.includes(kw)) {
        searchIndex.byCategory.get(cat)?.forEach((epId) => {
          scores.set(epId, (scores.get(epId) || 0) + 3);
        });
      }
    });
  });

  // Get top episodes
  const topEpisodes = [...scores.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([id]) => id);

  // If no matches, get a diverse sample
  if (topEpisodes.length < 10) {
    const allIds = Object.keys(analysisData);
    for (let i = 0; i < Math.min(20, allIds.length); i++) {
      if (!topEpisodes.includes(allIds[i])) {
        topEpisodes.push(allIds[i]);
      }
    }
  }

  return topEpisodes
    .map((id) => {
      const data = analysisData[id];
      return `
EPISODE: ${id}
Guest: ${data.guest_info?.name || "Unknown"} (${data.guest_info?.title || ""})
Topics: ${data.main_topics?.slice(0, 5).join(", ") || "N/A"}
Summary: ${data.episode_summary?.slice(0, 200) || "N/A"}
Problems: ${data.problems_addressed?.slice(0, 3).map((p) => `${p.specific_problem} @${p.timestamp}`).join("; ") || "N/A"}
Tactics: ${data.key_tactics?.slice(0, 3).map((t) => t.tactic).join("; ") || "N/A"}`;
    })
    .join("\n---\n");
}

const SYSTEM_PROMPT = `You are an AI assistant helping real estate agents find the most relevant podcast episodes for their specific challenges.

You have access to analyzed podcast episodes from "Keeping It Real" - a podcast with 700+ episodes interviewing top producing real estate agents.

Your job is to:
1. Understand the agent's specific challenge or situation
2. Match it to the most relevant episodes from the provided catalog
3. Provide specific timestamps where the relevant advice is discussed
4. Give a brief explanation of why each episode is relevant

Be specific and actionable. Focus on episodes that directly address the stated problem.

When responding, format your response as JSON with this structure:
{
  "recommendations": [
    {
      "episode_id": "the exact episode ID from the data",
      "guest_name": "guest name",
      "relevance_score": 1-10,
      "why_relevant": "brief explanation of why this episode helps",
      "key_moments": [
        {
          "timestamp": "MM:SS",
          "description": "what's discussed at this timestamp"
        }
      ],
      "key_quote": "a relevant quote if available"
    }
  ],
  "summary": "A brief 1-2 sentence summary of your recommendations"
}

Return ONLY valid JSON, no markdown or additional text.`;

export async function POST(request: NextRequest) {
  try {
    const { challenge } = await request.json();

    if (!challenge) {
      return NextResponse.json(
        { error: "Please describe the challenge" },
        { status: 400 }
      );
    }

    // Check for API key
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      // Fallback to local search if no API key
      return localSearch(challenge);
    }

    // Try OpenAI, fall back to local search on any error
    try {
      // Get relevant episode summaries for this challenge
      const relevantEpisodes = getRelevantEpisodeSummaries(challenge);

      const openai = new OpenAI({ apiKey });

      const response = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: SYSTEM_PROMPT },
          {
            role: "user",
            content: `An agent describes their challenge: "${challenge}"

Here are the most relevant episodes from our catalog:
${relevantEpisodes}

Find the top 3-5 most relevant episodes with specific timestamps. Use EXACT episode IDs from the data.`,
          },
        ],
        temperature: 0.3,
        max_tokens: 2000,
      });

      const content = response.choices[0]?.message?.content || "";

      // Parse JSON response
      let recommendations;
      try {
        const cleaned = content.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
        recommendations = JSON.parse(cleaned);
      } catch {
        // If AI response parsing fails, fall back to local search
        console.log("AI response parsing failed, using local search");
        return localSearch(challenge);
      }

      // Enrich with episode details
      const enriched = {
        ...recommendations,
        recommendations: recommendations.recommendations?.map(
          (rec: { episode_id: string; guest_name?: string }) => {
            const episodeData = analysisData[rec.episode_id];
            const episodeInfo = episodes.find(
              (ep) =>
                ep.guest_name
                  ?.toLowerCase()
                  .includes((rec.guest_name || "").toLowerCase().split(" ")[0]) ||
                ep.title?.includes(rec.episode_id)
            );

            return {
              ...rec,
              episode_url: episodeInfo?.guid || "#",
              full_title: episodeInfo?.title || "",
              duration: episodeInfo?.duration_formatted || "",
              guest_info: episodeData?.guest_info || {},
            };
          }
        ),
        method: "ai_search",
        episodes_searched: Object.keys(analysisData).length,
      };

      return NextResponse.json(enriched);
    } catch (aiError) {
      // OpenAI error (quota exceeded, rate limit, etc.) - fall back to local search
      console.log("OpenAI error, falling back to local search:", aiError);
      return localSearch(challenge);
    }
  } catch (error) {
    console.error("Recommendation error:", error);
    return NextResponse.json({ error: "Failed to get recommendations" }, { status: 500 });
  }
}

// Improved local search when no API key
function localSearch(challenge: string) {
  const keywords = challenge.toLowerCase().split(/\s+/).filter((w) => w.length > 2);
  const scores: Array<{ id: string; score: number; matches: string[] }> = [];

  for (const [id, data] of Object.entries(analysisData)) {
    let score = 0;
    const matches: string[] = [];

    // Search in topics (high weight)
    data.main_topics?.forEach((topic) => {
      keywords.forEach((kw) => {
        if (topic.toLowerCase().includes(kw)) {
          score += 5;
          if (!matches.includes(`Topic: ${topic}`)) {
            matches.push(`Topic: ${topic}`);
          }
        }
      });
    });

    // Search in problems (highest weight)
    data.problems_addressed?.forEach((problem) => {
      keywords.forEach((kw) => {
        if (
          problem.specific_problem.toLowerCase().includes(kw) ||
          problem.solution_summary.toLowerCase().includes(kw)
        ) {
          score += 8;
          if (!matches.includes(`Problem: ${problem.specific_problem}`)) {
            matches.push(`Problem: ${problem.specific_problem}`);
          }
        }
      });
    });

    // Search in tactics
    data.key_tactics?.forEach((tactic) => {
      keywords.forEach((kw) => {
        if (tactic.tactic.toLowerCase().includes(kw)) {
          score += 4;
          if (!matches.includes(`Tactic: ${tactic.tactic}`)) {
            matches.push(`Tactic: ${tactic.tactic}`);
          }
        }
      });
    });

    // Search in summary
    keywords.forEach((kw) => {
      if (data.episode_summary?.toLowerCase().includes(kw)) {
        score += 2;
      }
    });

    // Search in guest specialty
    keywords.forEach((kw) => {
      if (data.guest_info?.specialty?.toLowerCase().includes(kw)) {
        score += 6;
        matches.push(`Specialty: ${data.guest_info.specialty}`);
      }
    });

    if (score > 0) {
      scores.push({ id, score, matches: [...new Set(matches)] });
    }
  }

  // Sort by score and take top 5
  const top5 = scores.sort((a, b) => b.score - a.score).slice(0, 5);

  const recommendations = top5.map((item) => {
    const data = analysisData[item.id];
    const episodeInfo = episodes.find(
      (ep) =>
        ep.guest_name?.toLowerCase().includes((data.guest_info?.name || "").toLowerCase().split(" ")[0])
    );

    return {
      episode_id: item.id,
      guest_name: data.guest_info?.name || "Unknown",
      relevance_score: Math.min(10, Math.round(item.score / 3)),
      why_relevant: item.matches.slice(0, 3).join("; "),
      key_moments:
        data.problems_addressed?.slice(0, 2).map((p) => ({
          timestamp: p.timestamp,
          description: p.solution_summary,
        })) || [],
      key_quote: data.quotable_insights?.[0] || "",
      episode_url: episodeInfo?.guid || "#",
      full_title: episodeInfo?.title || "",
      duration: episodeInfo?.duration_formatted || "",
      guest_info: data.guest_info || {},
    };
  });

  return NextResponse.json({
    recommendations,
    summary: `Found ${recommendations.length} relevant episodes from ${Object.keys(analysisData).length} analyzed episodes.`,
    method: "local_search",
    episodes_searched: Object.keys(analysisData).length,
  });
}
