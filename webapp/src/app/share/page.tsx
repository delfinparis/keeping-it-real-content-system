"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import Link from "next/link";
import allAnalysis from "@/data/all_analysis.json";
import episodesData from "@/data/episodes.json";
import Footer from "@/components/Footer";

const episodes = episodesData.episodes;

interface AnalysisData {
  guest_info?: {
    name?: string | null;
    title?: string | null;
    company?: string | null;
  };
  episode_summary?: string;
  problems_addressed?: Array<{
    category: string;
    specific_problem: string;
    solution_summary: string;
    timestamp: string;
  }>;
  clip_worthy_moments?: Array<{
    timestamp: string;
    quote: string;
  }>;
}

const analysisData = allAnalysis as Record<string, AnalysisData>;

function ShareContent() {
  const searchParams = useSearchParams();
  const episodeIds = searchParams.get("episodes")?.split(",") || [];
  const challenge = searchParams.get("challenge") || "";
  const [copied, setCopied] = useState<string | null>(null);

  const copyToClipboard = async (text: string, type: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(null), 2000);
  };

  // Find episodes from the IDs
  const recommendations = episodeIds
    .map((id) => {
      const analysis = analysisData[id];
      if (!analysis) return null;

      // Find episode info
      const itemMatch = id.match(/item(\d+)/);
      const episodeNum = itemMatch ? parseInt(itemMatch[1]) : null;
      const episode = episodeNum
        ? episodes.find((ep) => ep.id === episodeNum)
        : episodes.find((ep) =>
            ep.guest_name?.toLowerCase().includes(
              (analysis.guest_info?.name || "").toLowerCase().split(" ")[0]
            )
          );

      return {
        id,
        analysis,
        episode,
      };
    })
    .filter(Boolean);

  if (recommendations.length === 0) {
    return (
      <main className="min-h-screen bg-gray-50 flex flex-col">
                <div className="flex-1 flex items-center justify-center">
          <div className="text-center p-8">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              No recommendations found
            </h1>
            <p className="text-gray-600 mb-6">
              This link may be invalid or the episodes may have been removed.
            </p>
            <Link
              href="/"
              className="bg-kale text-white px-6 py-3 rounded-lg font-medium hover:bg-kale-light transition inline-block"
            >
              Find Your Own Recommendations
            </Link>
          </div>
        </div>
        <Footer />
      </main>
    );
  }

  const shareUrl = typeof window !== "undefined" ? window.location.href : "";

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">
            {/* Page Header */}
      <div className="bg-gradient-kale text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center">
          <p className="text-blue-200 mb-2">Someone wants to help you get unstuck</p>
          <h1 className="text-3xl font-bold mb-4">
            Your Unstuck Agent Recommendations
          </h1>
          {challenge && (
            <p className="text-lg text-blue-100">
              For: "{challenge}"
            </p>
          )}
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1">
        {/* Share this collection */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h2 className="font-bold text-gray-900">Share this collection</h2>
              <p className="text-sm text-gray-500">
                {recommendations.length} episode{recommendations.length !== 1 ? "s" : ""} curated
                for this challenge
              </p>
            </div>
            <button
              onClick={() => copyToClipboard(shareUrl, "share")}
              className={`px-6 py-3 rounded-lg font-medium transition ${
                copied === "share"
                  ? "bg-green-600 text-white"
                  : "bg-kale text-white hover:bg-kale-light"
              }`}
            >
              {copied === "share" ? "✓ Copied!" : "📋 Copy Link"}
            </button>
          </div>
        </div>

        {/* Episodes */}
        <div className="space-y-6">
          {recommendations.map((rec, idx) => {
            if (!rec) return null;
            const { id, analysis, episode } = rec;

            return (
              <div
                key={id}
                className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
              >
                <div className="bg-gradient-to-r from-blue-50 to-white px-6 py-4 border-b border-gray-200">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-4">
                      <div className="bg-kale text-white w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg">
                        {idx + 1}
                      </div>
                      <div>
                        <h3 className="font-bold text-xl text-gray-900">
                          {analysis.guest_info?.name || "Unknown Guest"}
                        </h3>
                        {analysis.guest_info?.title && (
                          <p className="text-gray-500 text-sm">
                            {analysis.guest_info.title}
                            {analysis.guest_info.company &&
                              ` at ${analysis.guest_info.company}`}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="p-6">
                  {analysis.episode_summary && (
                    <p className="text-gray-700 mb-4">{analysis.episode_summary}</p>
                  )}

                  {analysis.problems_addressed && analysis.problems_addressed.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">
                        🎯 Key Timestamps:
                      </h4>
                      <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                        {analysis.problems_addressed.slice(0, 3).map((p, pIdx) => (
                          <div key={pIdx} className="flex items-start gap-3">
                            <span className="bg-kale text-white px-2 py-1 rounded text-xs font-mono font-bold">
                              {p.timestamp}
                            </span>
                            <p className="text-sm text-gray-700">{p.specific_problem}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {analysis.clip_worthy_moments && analysis.clip_worthy_moments.length > 0 && (
                    <blockquote className="border-l-4 border-kale pl-4 italic text-gray-600 mb-4">
                      "{analysis.clip_worthy_moments[0].quote}"
                    </blockquote>
                  )}

                  <div className="flex flex-wrap gap-2">
                    {episode?.guid && (
                      <a
                        href={episode.guid}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-kale text-white px-4 py-2 rounded-lg font-medium hover:bg-kale-light transition"
                      >
                        🎧 Listen Now
                      </a>
                    )}
                    {episode && (
                      <Link
                        href={`/episodes/${episode.id}`}
                        className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200 transition"
                      >
                        View Full Details
                      </Link>
                    )}
                    <button
                      onClick={() =>
                        copyToClipboard(episode?.guid || shareUrl, `episode-${idx}`)
                      }
                      className={`px-4 py-2 rounded-lg font-medium transition ${
                        copied === `episode-${idx}`
                          ? "bg-green-600 text-white"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                      }`}
                    >
                      {copied === `episode-${idx}` ? "✓ Copied" : "📋 Copy Link"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* CTA */}
        <div className="mt-12 text-center bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Need your own recommendations?
          </h2>
          <p className="text-gray-600 mb-6">
            Tell us about your challenge and we'll find the perfect episodes
          </p>
          <Link
            href="/"
            className="inline-flex items-center gap-2 bg-kale text-white px-8 py-4 rounded-xl font-semibold hover:bg-kale-light transition"
          >
            <span>Find Episodes for Me</span>
            <span>→</span>
          </Link>
        </div>
      </div>

      <Footer />
    </main>
  );
}

export default function SharePage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-gray-50 flex flex-col">
                    <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="w-12 h-12 border-4 border-kale border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-gray-600">Loading recommendations...</p>
            </div>
          </div>
          <Footer />
        </div>
      }
    >
      <ShareContent />
    </Suspense>
  );
}
