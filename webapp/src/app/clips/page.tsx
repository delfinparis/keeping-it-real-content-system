"use client";

import { useState } from "react";
import Link from "next/link";
import episodesData from "@/data/episodes.json";

// Import clip files
import clips1 from "@/data/analysis/2025-12-22_item5_Chris-Linsell_analysis.json";
import clips2 from "@/data/analysis/2025-12-30_item4_Connie-Mahan_analysis.json";
import clips3 from "@/data/analysis/2026-01-05_item3_Tim-Burrell_analysis.json";
import clips4 from "@/data/analysis/2026-01-21_item2_Marisa-Kashino_analysis.json";
import clips5 from "@/data/analysis/2026-01-22_item1_Kristee-Leonard_analysis.json";

const episodes = episodesData.episodes;

interface Clip {
  timestamp: string;
  end_timestamp: string;
  quote: string;
  clip_type: string;
  why_clipworthy: string;
  suggested_hook: string;
}

interface AnalysisWithClips {
  guest_info?: { name?: string | null };
  clip_worthy_moments?: Clip[];
}

const allAnalysis: { id: string; data: AnalysisWithClips }[] = [
  { id: "2025-12-22_item5_Chris-Linsell", data: clips1 as AnalysisWithClips },
  { id: "2025-12-30_item4_Connie-Mahan", data: clips2 as AnalysisWithClips },
  { id: "2026-01-05_item3_Tim-Burrell", data: clips3 as AnalysisWithClips },
  { id: "2026-01-21_item2_Marisa-Kashino", data: clips4 as AnalysisWithClips },
  { id: "2026-01-22_item1_Kristee-Leonard", data: clips5 as AnalysisWithClips },
];

const CLIP_TYPES = [
  { id: "tactical_specificity", name: "Tactical", icon: "🎯", description: "Specific, actionable advice" },
  { id: "contrarian_take", name: "Contrarian", icon: "🔄", description: "Goes against conventional wisdom" },
  { id: "emotional_resonance", name: "Emotional", icon: "❤️", description: "Stories that hit you in the gut" },
  { id: "memorable_oneliner", name: "One-Liner", icon: "💬", description: "Quotable phrases" },
  { id: "pattern_reveal", name: "Pattern", icon: "📊", description: "What top producers do differently" },
  { id: "surprising_statistic", name: "Stats", icon: "📈", description: "Numbers that make you stop" },
  { id: "permission_slip", name: "Permission", icon: "✅", description: "Frees agents from guilt" },
  { id: "mindset_shift", name: "Mindset", icon: "🧠", description: "Reframes how you see business" },
];

export default function ClipsPage() {
  const [filterType, setFilterType] = useState<string>("all");
  const [copied, setCopied] = useState<string | null>(null);

  // Gather all clips
  const allClips = allAnalysis.flatMap(({ id, data }) => {
    const guestName = data.guest_info?.name || id.split("_")[2]?.replace(/-/g, " ") || "Unknown";
    const episode = episodes.find(ep => ep.guest_name?.toLowerCase().includes(guestName.toLowerCase().split(" ")[0]));

    return (data.clip_worthy_moments || []).map((clip, idx) => ({
      ...clip,
      episodeId: id,
      guestName,
      episodeUrl: episode?.guid || "#",
      episodeDbId: episode?.id,
      clipId: `${id}-${idx}`,
    }));
  });

  // Filter clips
  const filteredClips = filterType === "all"
    ? allClips
    : allClips.filter(clip => clip.clip_type === filterType);

  const copyClip = async (clip: typeof allClips[0]) => {
    const text = `🎬 CLIP: ${clip.guestName}\n\n"${clip.quote}"\n\n⏱️ Timestamp: ${clip.timestamp}\n🎯 Hook: ${clip.suggested_hook}\n\n🔗 ${clip.episodeUrl}`;
    await navigator.clipboard.writeText(text);
    setCopied(clip.clipId);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-900">🎬 Clips Gallery</h1>
          <p className="text-gray-600 mt-2">
            {allClips.length} clip-worthy moments ready for short-form video content
          </p>
        </div>
      </div>

      {/* Filter */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <h3 className="font-medium text-gray-900 mb-3">Filter by Clip Type</h3>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setFilterType("all")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                filterType === "all"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              All ({allClips.length})
            </button>
            {CLIP_TYPES.map(type => {
              const count = allClips.filter(c => c.clip_type === type.id).length;
              if (count === 0) return null;
              return (
                <button
                  key={type.id}
                  onClick={() => setFilterType(type.id)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    filterType === type.id
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {type.icon} {type.name} ({count})
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Clips Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredClips.map((clip) => {
            const clipType = CLIP_TYPES.find(t => t.id === clip.clip_type);
            return (
              <div
                key={clip.clipId}
                className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
              >
                {/* Clip Header */}
                <div className="bg-gradient-to-r from-purple-50 to-white px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{clipType?.icon || "🎬"}</span>
                      <div>
                        <span className="font-medium text-gray-900">{clip.guestName}</span>
                        <span className="text-gray-400 mx-2">•</span>
                        <span className="text-purple-600 text-sm font-medium">
                          {clipType?.name || clip.clip_type.replace(/_/g, " ")}
                        </span>
                      </div>
                    </div>
                    <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg text-sm font-mono">
                      {clip.timestamp}
                    </span>
                  </div>
                </div>

                {/* Clip Content */}
                <div className="p-6">
                  {/* Quote */}
                  <blockquote className="border-l-4 border-purple-500 pl-4 italic text-gray-700 text-lg mb-4">
                    "{clip.quote}"
                  </blockquote>

                  {/* Hook */}
                  <div className="mb-4">
                    <span className="text-sm font-medium text-gray-500">Suggested Hook:</span>
                    <p className="text-gray-900">{clip.suggested_hook}</p>
                  </div>

                  {/* Why Clipworthy */}
                  <div className="mb-4">
                    <span className="text-sm font-medium text-gray-500">Why it works:</span>
                    <p className="text-gray-600 text-sm">{clip.why_clipworthy}</p>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-wrap gap-2 pt-4 border-t border-gray-100">
                    <button
                      onClick={() => copyClip(clip)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2 ${
                        copied === clip.clipId
                          ? "bg-green-600 text-white"
                          : "bg-blue-600 text-white hover:bg-blue-700"
                      }`}
                    >
                      {copied === clip.clipId ? "✓ Copied!" : "📋 Copy Clip Info"}
                    </button>
                    {clip.episodeDbId && (
                      <Link
                        href={`/episodes/${clip.episodeDbId}`}
                        className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
                      >
                        View Episode
                      </Link>
                    )}
                    <a
                      href={clip.episodeUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-gray-800 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-900 transition"
                    >
                      🎧 Listen
                    </a>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {filteredClips.length === 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <p className="text-gray-500">No clips found for this filter.</p>
          </div>
        )}
      </div>

      {/* Content Pillar Guide */}
      <div className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h2 className="text-2xl font-bold mb-6">Content Pillars for Social Media</h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="bg-gray-800 rounded-lg p-4">
              <span className="text-2xl">🤖</span>
              <h3 className="font-medium mt-2">AI Agent</h3>
              <p className="text-gray-400 text-sm">Tech & AI tactics</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-4">
              <span className="text-2xl">🏆</span>
              <h3 className="font-medium mt-2">Top Producer</h3>
              <p className="text-gray-400 text-sm">Proven strategies</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-4">
              <span className="text-2xl">💬</span>
              <h3 className="font-medium mt-2">Real Talk</h3>
              <p className="text-gray-400 text-sm">Mindset & emotion</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-4">
              <span className="text-2xl">📊</span>
              <h3 className="font-medium mt-2">Market Intel</h3>
              <p className="text-gray-400 text-sm">Industry insights</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-4">
              <span className="text-2xl">⚙️</span>
              <h3 className="font-medium mt-2">Systems</h3>
              <p className="text-gray-400 text-sm">Productivity tips</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
