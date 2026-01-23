import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
import episodesData from "@/data/episodes.json";
const episodes = episodesData.episodes;
import problemMap from "@/data/problem_episode_map.json";
import avatarMap from "@/data/avatar_episode_map.json";

// Import all analysis files
import analysis1 from "@/data/analysis/2025-12-22_item5_Chris-Linsell_analysis.json";
import analysis2 from "@/data/analysis/2025-12-30_item4_Connie-Mahan_analysis.json";
import analysis3 from "@/data/analysis/2026-01-05_item3_Tim-Burrell_analysis.json";
import analysis4 from "@/data/analysis/2026-01-21_item2_Marisa-Kashino_analysis.json";
import analysis5 from "@/data/analysis/2026-01-22_item1_Kristee-Leonard_analysis.json";

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

const analysisData: Record<string, AnalysisData> = {
  "2025-12-22_item5_Chris-Linsell": analysis1 as AnalysisData,
  "2025-12-30_item4_Connie-Mahan": analysis2 as AnalysisData,
  "2026-01-05_item3_Tim-Burrell": analysis3 as AnalysisData,
  "2026-01-21_item2_Marisa-Kashino": analysis4 as AnalysisData,
  "2026-01-22_item1_Kristee-Leonard": analysis5 as AnalysisData,
};

const SYSTEM_PROMPT = `You are an AI assistant helping real estate agents find the most relevant podcast episodes for their specific challenges.

You have access to analyzed podcast episodes from "Keeping It Real" - a podcast with 700+ episodes interviewing top producing real estate agents.

Your job is to:
1. Understand the agent's specific challenge or situation
2. Match it to the most relevant episodes from our analyzed catalog
3. Provide specific timestamps where the relevant advice is discussed
4. Give a brief explanation of why each episode is relevant

Be specific and actionable. Focus on episodes that directly address the stated problem.

Available analyzed episodes and their content:
${Object.entries(analysisData).map(([id, data]) => `
EPISODE: ${id}
Guest: ${data.guest_info?.name || 'Unknown'}
Topics: ${data.main_topics?.join(', ') || 'N/A'}
Summary: ${data.episode_summary || 'N/A'}
Problems Addressed:
${data.problems_addressed?.map(p => `- ${p.specific_problem} (${p.timestamp}): ${p.solution_summary}`).join('\n') || 'N/A'}
Key Tactics:
${data.key_tactics?.map(t => `- ${t.tactic} (${t.timestamp})`).join('\n') || 'N/A'}
Clip-worthy moments:
${data.clip_worthy_moments?.map(c => `- "${c.quote}" (${c.timestamp})`).join('\n') || 'N/A'}
`).join('\n---\n')}

When responding, format your response as JSON with this structure:
{
  "recommendations": [
    {
      "episode_id": "the episode ID",
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

    const openai = new OpenAI({ apiKey });

    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        {
          role: "user",
          content: `An agent describes their challenge: "${challenge}"\n\nFind the top 3 most relevant episodes with specific timestamps.`,
        },
      ],
      temperature: 0.3,
      max_tokens: 1500,
    });

    const content = response.choices[0]?.message?.content || "";

    // Parse JSON response
    let recommendations;
    try {
      // Clean up potential markdown formatting
      const cleaned = content.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
      recommendations = JSON.parse(cleaned);
    } catch {
      return NextResponse.json(
        { error: "Failed to parse AI response", raw: content },
        { status: 500 }
      );
    }

    // Enrich with episode details
    const enriched = {
      ...recommendations,
      recommendations: recommendations.recommendations?.map((rec: { episode_id: string; guest_name?: string }) => {
        const episodeData = analysisData[rec.episode_id];
        const episodeInfo = episodes.find(
          (ep) => ep.guest_name?.toLowerCase().includes((rec.guest_name || "").toLowerCase().split(" ")[0])
        );

        return {
          ...rec,
          episode_url: episodeInfo?.guid || "#",
          full_title: episodeInfo?.title || "",
          duration: episodeInfo?.duration_formatted || "",
          guest_info: episodeData?.guest_info || {},
        };
      }),
    };

    return NextResponse.json(enriched);
  } catch (error) {
    console.error("Recommendation error:", error);
    return NextResponse.json(
      { error: "Failed to get recommendations" },
      { status: 500 }
    );
  }
}

// Fallback local search when no API key
function localSearch(challenge: string) {
  const keywords = challenge.toLowerCase().split(/\s+/);
  const scores: Array<{ id: string; score: number; matches: string[] }> = [];

  for (const [id, data] of Object.entries(analysisData)) {
    let score = 0;
    const matches: string[] = [];

    // Search in topics
    data.main_topics?.forEach((topic) => {
      keywords.forEach((kw) => {
        if (topic.toLowerCase().includes(kw)) {
          score += 3;
          matches.push(`Topic: ${topic}`);
        }
      });
    });

    // Search in problems
    data.problems_addressed?.forEach((problem) => {
      keywords.forEach((kw) => {
        if (problem.specific_problem.toLowerCase().includes(kw) ||
            problem.solution_summary.toLowerCase().includes(kw)) {
          score += 5;
          matches.push(`Problem: ${problem.specific_problem}`);
        }
      });
    });

    // Search in tactics
    data.key_tactics?.forEach((tactic) => {
      keywords.forEach((kw) => {
        if (tactic.tactic.toLowerCase().includes(kw)) {
          score += 2;
          matches.push(`Tactic: ${tactic.tactic}`);
        }
      });
    });

    // Search in summary
    keywords.forEach((kw) => {
      if (data.episode_summary?.toLowerCase().includes(kw)) {
        score += 1;
      }
    });

    if (score > 0) {
      scores.push({ id, score, matches: [...new Set(matches)] });
    }
  }

  // Sort by score and take top 3
  const top3 = scores.sort((a, b) => b.score - a.score).slice(0, 3);

  const recommendations = top3.map((item) => {
    const data = analysisData[item.id];
    const episodeInfo = episodes.find(
      (ep) => ep.guest_name?.toLowerCase().includes((data.guest_info?.name || "").toLowerCase().split(" ")[0])
    );

    return {
      episode_id: item.id,
      guest_name: data.guest_info?.name || "Unknown",
      relevance_score: Math.min(10, Math.round(item.score)),
      why_relevant: item.matches.slice(0, 3).join("; "),
      key_moments: data.problems_addressed?.slice(0, 2).map((p) => ({
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
    summary: `Found ${recommendations.length} relevant episodes based on keyword matching.`,
    method: "local_search",
  });
}
