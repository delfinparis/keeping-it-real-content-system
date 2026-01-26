"use client";

import { useState, use } from "react";
import Link from "next/link";
import episodesData from "@/data/episodes.json";
import allAnalysis from "@/data/all_analysis.json";
import { PROBLEM_CATEGORIES, AVATARS } from "@/lib/types";

const episodes = episodesData.episodes;

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

// Find analysis by episode ID or filename pattern
function findAnalysis(episodeId: number, guestName?: string): AnalysisData | null {
  // Try to find by matching the episode number in the filename
  for (const [key, data] of Object.entries(analysisData)) {
    // Match patterns like "2025-12-22_item5_Chris-Linsell"
    const itemMatch = key.match(/item(\d+)/);
    if (itemMatch && parseInt(itemMatch[1]) === episodeId) {
      return data;
    }
    // Also try matching by guest name
    if (guestName && key.toLowerCase().includes(guestName.toLowerCase().split(" ")[0])) {
      return data;
    }
  }
  return null;
}

// Get the analysis key for linking
function getAnalysisKey(episodeId: number, guestName?: string): string | null {
  for (const key of Object.keys(analysisData)) {
    const itemMatch = key.match(/item(\d+)/);
    if (itemMatch && parseInt(itemMatch[1]) === episodeId) {
      return key;
    }
    if (guestName && key.toLowerCase().includes(guestName.toLowerCase().split(" ")[0])) {
      return key;
    }
  }
  return null;
}

type Props = {
  params: Promise<{ id: string }>;
};

export default function EpisodeDetailPage({ params }: Props) {
  const { id } = use(params);
  const episodeId = parseInt(id, 10);
  const episode = episodes.find((ep) => ep.id === episodeId);
  const analysis = episode ? findAnalysis(episodeId, episode.guest_name || undefined) : null;
  const analysisKey = episode ? getAnalysisKey(episodeId, episode.guest_name || undefined) : null;

  const [copied, setCopied] = useState<string | null>(null);

  if (!episode) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold text-gray-900">Episode not found</h1>
        <Link href="/episodes" className="text-kale hover:underline mt-4 inline-block">
          Browse all episodes
        </Link>
      </div>
    );
  }

  const copyToClipboard = async (text: string, type: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(null), 2000);
  };

  const shareUrl = typeof window !== "undefined"
    ? `${window.location.origin}/episodes/${episodeId}`
    : `/episodes/${episodeId}`;

  const shareMessage = analysis
    ? `Check out this episode of Keeping It Real with ${episode.guest_name}: ${analysis.episode_summary?.slice(0, 100)}...`
    : `Check out this episode of Keeping It Real with ${episode.guest_name}`;

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link href="/episodes" className="text-kale hover:underline text-sm mb-4 inline-block">
            ← Back to all episodes
          </Link>

          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-sm text-gray-500">{episode.publish_date}</span>
                {episode.duration_formatted && (
                  <span className="text-sm text-gray-500">⏱️ {episode.duration_formatted}</span>
                )}
                {analysis && (
                  <span className="bg-green-100 text-green-800 px-2 py-0.5 rounded text-xs font-medium">
                    Analyzed
                  </span>
                )}
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {episode.guest_name || "Unknown Guest"}
              </h1>
              <p className="text-xl text-gray-600">{episode.title}</p>

              {analysis?.guest_info && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {analysis.guest_info.title && (
                    <span className="bg-kale-50 text-kale px-3 py-1 rounded-full text-sm">
                      {analysis.guest_info.title}
                    </span>
                  )}
                  {analysis.guest_info.company && (
                    <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">
                      {analysis.guest_info.company}
                    </span>
                  )}
                  {analysis.guest_info.location && (
                    <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">
                      📍 {analysis.guest_info.location}
                    </span>
                  )}
                  {analysis.guest_info.production_level && (
                    <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                      {analysis.guest_info.production_level}
                    </span>
                  )}
                </div>
              )}
            </div>

            <div className="flex flex-col gap-2">
              <a
                href={episode.guid}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-kale text-white px-6 py-3 rounded-lg font-medium hover:bg-kale-light transition text-center"
              >
                🎧 Listen Now
              </a>
              <button
                onClick={() => copyToClipboard(episode.guid, "link")}
                className={`px-6 py-3 rounded-lg font-medium transition text-center ${
                  copied === "link"
                    ? "bg-green-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {copied === "link" ? "✓ Copied!" : "📋 Copy Episode Link"}
              </button>
              <button
                onClick={() => copyToClipboard(shareUrl, "share")}
                className={`px-6 py-3 rounded-lg font-medium transition text-center ${
                  copied === "share"
                    ? "bg-green-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {copied === "share" ? "✓ Copied!" : "🔗 Copy Share Link"}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Summary */}
            {analysis?.episode_summary && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Episode Summary</h2>
                <p className="text-gray-700 leading-relaxed">{analysis.episode_summary}</p>
              </div>
            )}

            {/* Key Timestamps */}
            {analysis?.problems_addressed && analysis.problems_addressed.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">🎯 Key Timestamps</h2>
                <div className="space-y-4">
                  {analysis.problems_addressed.map((problem, idx) => (
                    <div key={idx} className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                      <span className="bg-kale text-white px-3 py-1 rounded-lg text-sm font-mono font-bold whitespace-nowrap">
                        {problem.timestamp}
                      </span>
                      <div>
                        <p className="font-medium text-gray-900">{problem.specific_problem}</p>
                        <p className="text-gray-600 text-sm mt-1">{problem.solution_summary}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Clip-Worthy Moments */}
            {analysis?.clip_worthy_moments && analysis.clip_worthy_moments.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">🎬 Clip-Worthy Moments</h2>
                <div className="space-y-4">
                  {analysis.clip_worthy_moments.map((clip, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs font-medium">
                          {clip.clip_type.replace(/_/g, " ")}
                        </span>
                        <span className="text-gray-500 text-sm">
                          {clip.timestamp} - {clip.end_timestamp}
                        </span>
                      </div>
                      <blockquote className="border-l-4 border-kale pl-4 italic text-gray-700 mb-2">
                        "{clip.quote}"
                      </blockquote>
                      <p className="text-sm text-gray-600">
                        <strong>Hook:</strong> {clip.suggested_hook}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Key Tactics */}
            {analysis?.key_tactics && analysis.key_tactics.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">💡 Key Tactics</h2>
                <div className="space-y-3">
                  {analysis.key_tactics.map((tactic, idx) => (
                    <div key={idx} className="flex items-start gap-3">
                      <span className="text-kale font-bold">•</span>
                      <div>
                        <p className="text-gray-900">{tactic.tactic}</p>
                        <p className="text-gray-500 text-sm">
                          {tactic.context} ({tactic.timestamp})
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Quotable Insights */}
            {analysis?.quotable_insights && analysis.quotable_insights.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">💬 Quotable Insights</h2>
                <div className="space-y-4">
                  {analysis.quotable_insights.map((quote, idx) => (
                    <div key={idx} className="relative">
                      <blockquote className="border-l-4 border-yellow-500 pl-4 italic text-gray-700">
                        "{quote}"
                      </blockquote>
                      <button
                        onClick={() => copyToClipboard(quote, `quote-${idx}`)}
                        className={`mt-2 text-xs px-2 py-1 rounded ${
                          copied === `quote-${idx}`
                            ? "bg-green-100 text-green-700"
                            : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                        }`}
                      >
                        {copied === `quote-${idx}` ? "✓ Copied" : "Copy quote"}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Description */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Full Description</h2>
              <div
                className="prose prose-gray max-w-none"
                dangerouslySetInnerHTML={{
                  __html: episode.full_description || episode.description || "",
                }}
              />
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Share Card */}
            <div className="bg-gradient-to-br from-kale to-kale-light rounded-xl p-6 text-white">
              <h3 className="font-bold mb-3">Share This Episode</h3>
              <p className="text-sm text-blue-100 mb-4">
                Send this episode to an agent who needs it
              </p>
              <button
                onClick={() => {
                  const text = `${shareMessage}\n\n${shareUrl}`;
                  copyToClipboard(text, "full-share");
                }}
                className={`w-full py-2 rounded-lg font-medium transition ${
                  copied === "full-share"
                    ? "bg-green-500 text-white"
                    : "bg-white text-kale hover:bg-blue-50"
                }`}
              >
                {copied === "full-share" ? "✓ Ready to paste!" : "📤 Copy to share"}
              </button>
            </div>

            {/* Topics */}
            {analysis?.main_topics && analysis.main_topics.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-3">Topics Covered</h3>
                <div className="flex flex-wrap gap-2">
                  {analysis.main_topics.map((topic, idx) => (
                    <span
                      key={idx}
                      className="bg-kale-50 text-kale px-3 py-1 rounded-full text-sm"
                    >
                      {topic}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Problems Addressed */}
            {analysis?.problems_addressed && analysis.problems_addressed.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-3">Problems Addressed</h3>
                <div className="space-y-2">
                  {[...new Set(analysis.problems_addressed.map((p) => p.category))].map(
                    (category) => {
                      const cat = PROBLEM_CATEGORIES[category];
                      return (
                        <Link
                          key={category}
                          href={`/problems/${category}`}
                          className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-50 transition"
                        >
                          <span>{cat?.icon || "📌"}</span>
                          <span className="text-gray-700">{cat?.name || category}</span>
                        </Link>
                      );
                    }
                  )}
                </div>
              </div>
            )}

            {/* Target Avatars */}
            {analysis?.target_avatars && analysis.target_avatars.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-3">Best For</h3>
                <div className="space-y-3">
                  {analysis.target_avatars.map((avatar, idx) => {
                    const av = AVATARS[avatar.avatar_id];
                    return (
                      <Link
                        key={idx}
                        href={`/avatars/${avatar.avatar_id}`}
                        className="block p-3 rounded-lg bg-gray-50 hover:bg-kale-50 transition"
                      >
                        <div className="flex items-center gap-2 mb-1">
                          <span>{av?.icon || "👤"}</span>
                          <span className="font-medium text-gray-900">
                            {av?.name || avatar.avatar_id}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600">{avatar.key_takeaway}</p>
                      </Link>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Resources */}
            {analysis?.resources_mentioned && analysis.resources_mentioned.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-3">Resources Mentioned</h3>
                <div className="space-y-2">
                  {analysis.resources_mentioned.map((resource, idx) => (
                    <div key={idx} className="p-2">
                      <p className="font-medium text-gray-900">{resource.name}</p>
                      <p className="text-sm text-gray-500">
                        {resource.type} • {resource.context}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Not Analyzed Notice */}
            {!analysis && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
                <h3 className="font-bold text-yellow-800 mb-2">⚠️ Not Yet Analyzed</h3>
                <p className="text-yellow-700 text-sm">
                  This episode hasn't been analyzed yet. Key timestamps, clips, and insights
                  will appear here once processed.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
