"use client";

import { useState } from "react";
import Link from "next/link";
import { PROBLEM_CATEGORIES, AVATARS } from "@/lib/types";

interface KeyMoment {
  timestamp: string;
  description: string;
}

interface Recommendation {
  episode_id: string;
  guest_name: string;
  relevance_score: number;
  why_relevant: string;
  key_moments: KeyMoment[];
  key_quote: string;
  episode_url: string;
  full_title: string;
  duration: string;
  guest_info: {
    name?: string;
    title?: string;
    company?: string;
    specialty?: string;
  };
}

interface RecommendationResponse {
  recommendations: Recommendation[];
  summary: string;
  method?: string;
}

export default function Home() {
  const [challenge, setChallenge] = useState("");
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const getRecommendations = async () => {
    if (!challenge.trim()) return;

    setLoading(true);
    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ challenge }),
      });
      const data = await res.json();
      setRecommendations(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const copyLink = async (url: string, id: string) => {
    await navigator.clipboard.writeText(url);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  const copyAllLinks = async () => {
    if (!recommendations) return;
    const links = recommendations.recommendations
      .map((r, i) => `${i + 1}. ${r.guest_name}: ${r.episode_url}`)
      .join("\n");
    await navigator.clipboard.writeText(links);
    setCopied("all");
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <main className="min-h-screen">
      {/* Hero Section with AI Search */}
      <div className="bg-gradient-to-br from-blue-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            What's your agent's biggest challenge?
          </h1>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl">
            Describe their situation and I'll find the exact episodes (with timestamps) that solve their problem.
          </p>

          {/* AI Search Input */}
          <div className="max-w-2xl">
            <textarea
              placeholder="Example: 'They've been in the business for 3 years, doing about 10 deals a year, but can't seem to break through to the next level. They're working tons of hours but not seeing the results. Their main struggle is lead generation - they feel like their sphere is tapped out.'"
              value={challenge}
              onChange={(e) => setChallenge(e.target.value)}
              rows={4}
              className="w-full px-6 py-4 rounded-xl text-gray-900 text-lg focus:outline-none focus:ring-4 focus:ring-blue-300 resize-none"
            />
            <button
              onClick={getRecommendations}
              disabled={loading || !challenge.trim()}
              className="mt-4 w-full bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Finding the perfect episodes...
                </span>
              ) : (
                "🎯 Get Episode Recommendations"
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Recommendations Results */}
      {recommendations && recommendations.recommendations?.length > 0 && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                Top {recommendations.recommendations.length} Episode Recommendations
              </h2>
              <p className="text-gray-600 mt-1">{recommendations.summary}</p>
            </div>
            <button
              onClick={copyAllLinks}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition flex items-center space-x-2"
            >
              {copied === "all" ? (
                <>
                  <span>✓</span>
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <span>📋</span>
                  <span>Copy All Links</span>
                </>
              )}
            </button>
          </div>

          <div className="space-y-6">
            {recommendations.recommendations.map((rec, idx) => (
              <div
                key={rec.episode_id}
                className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden"
              >
                {/* Episode Header */}
                <div className="bg-gradient-to-r from-blue-50 to-white px-6 py-4 border-b border-gray-200">
                  <div className="flex justify-between items-start">
                    <div className="flex items-center space-x-4">
                      <div className="bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg">
                        {idx + 1}
                      </div>
                      <div>
                        <h3 className="font-bold text-xl text-gray-900">{rec.guest_name}</h3>
                        {rec.guest_info?.title && (
                          <p className="text-gray-500 text-sm">
                            {rec.guest_info.title}
                            {rec.guest_info.company && ` at ${rec.guest_info.company}`}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                        {rec.relevance_score}/10 Match
                      </span>
                      {rec.duration && (
                        <span className="text-gray-500 text-sm">⏱️ {rec.duration}</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Episode Content */}
                <div className="p-6">
                  {/* Why Relevant */}
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Why This Episode Helps:</h4>
                    <p className="text-gray-700">{rec.why_relevant}</p>
                  </div>

                  {/* Key Moments with Timestamps */}
                  {rec.key_moments?.length > 0 && (
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">🎯 Jump to These Timestamps:</h4>
                      <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                        {rec.key_moments.map((moment, mIdx) => (
                          <div key={mIdx} className="flex items-start space-x-3">
                            <span className="bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-mono font-bold whitespace-nowrap">
                              {moment.timestamp}
                            </span>
                            <p className="text-gray-700">{moment.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Key Quote */}
                  {rec.key_quote && (
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">💬 Key Quote:</h4>
                      <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-600">
                        "{rec.key_quote}"
                      </blockquote>
                    </div>
                  )}

                  {/* Episode Link - Prominent */}
                  <div className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-gray-500 mb-1">Episode Link (copy and send to agent):</p>
                        <p className="text-blue-600 font-mono text-sm truncate">{rec.episode_url}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => copyLink(rec.episode_url, rec.episode_id)}
                          className={`px-6 py-3 rounded-lg font-medium transition flex items-center space-x-2 ${
                            copied === rec.episode_id
                              ? "bg-green-600 text-white"
                              : "bg-blue-600 text-white hover:bg-blue-700"
                          }`}
                        >
                          {copied === rec.episode_id ? (
                            <>
                              <span>✓</span>
                              <span>Copied!</span>
                            </>
                          ) : (
                            <>
                              <span>📋</span>
                              <span>Copy Link</span>
                            </>
                          )}
                        </button>
                        <a
                          href={rec.episode_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="bg-gray-800 text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-900 transition"
                        >
                          🎧 Listen
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Quick Copy Template */}
          <div className="mt-8 bg-white rounded-xl shadow-lg border border-gray-200 p-6">
            <h3 className="font-bold text-lg text-gray-900 mb-4">📧 Quick Message Template</h3>
            <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm text-gray-700 whitespace-pre-wrap">
{`Hey! Based on what you told me about your challenges, I found some episodes from my podcast that directly address this:

${recommendations.recommendations.map((r, i) => `${i + 1}. ${r.guest_name} - ${r.why_relevant}
   Listen here: ${r.episode_url}
   Jump to: ${r.key_moments?.[0]?.timestamp || 'Start'} for the key insight`).join('\n\n')}

Let me know what you think after listening!`}
            </div>
            <button
              onClick={async () => {
                const template = `Hey! Based on what you told me about your challenges, I found some episodes from my podcast that directly address this:\n\n${recommendations.recommendations.map((r, i) => `${i + 1}. ${r.guest_name} - ${r.why_relevant}\n   Listen here: ${r.episode_url}\n   Jump to: ${r.key_moments?.[0]?.timestamp || 'Start'} for the key insight`).join('\n\n')}\n\nLet me know what you think after listening!`;
                await navigator.clipboard.writeText(template);
                setCopied("template");
                setTimeout(() => setCopied(null), 2000);
              }}
              className={`mt-4 px-6 py-3 rounded-lg font-medium transition ${
                copied === "template"
                  ? "bg-green-600 text-white"
                  : "bg-blue-600 text-white hover:bg-blue-700"
              }`}
            >
              {copied === "template" ? "✓ Copied Template!" : "📋 Copy Full Message"}
            </button>
          </div>
        </div>
      )}

      {/* No Results */}
      {recommendations && recommendations.recommendations?.length === 0 && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <p className="text-gray-500 text-lg">
              No matching episodes found. Try describing the challenge differently or browse by category below.
            </p>
          </div>
        </div>
      )}

      {/* Browse Section (shown when no search active) */}
      {!recommendations && (
        <>
          {/* Problem Categories Section */}
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Or Browse by Challenge Category
            </h2>
            <p className="text-gray-600 mb-8">
              Click a category to find episodes that address specific problems
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(PROBLEM_CATEGORIES).map(([key, category]) => (
                <Link
                  key={key}
                  href={`/problems/${key}`}
                  className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md hover:border-blue-300 transition group"
                >
                  <div className="flex items-start space-x-4">
                    <span className="text-3xl">{category.icon}</span>
                    <div>
                      <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition">
                        {category.name}
                      </h3>
                      <p className="text-sm text-gray-500 mt-1">
                        {category.description}
                      </p>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* Avatar Section */}
          <div className="bg-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Or Browse by Agent Type
              </h2>
              <p className="text-gray-600 mb-8">
                Get episode recommendations based on where the agent is in their career
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(AVATARS).map(([key, avatar]) => (
                  <Link
                    key={key}
                    href={`/avatars/${key}`}
                    className="bg-gray-50 rounded-xl p-6 border border-gray-200 hover:bg-blue-50 hover:border-blue-300 transition group"
                  >
                    <div className="flex items-start space-x-4">
                      <span className="text-3xl">{avatar.icon}</span>
                      <div>
                        <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition">
                          {avatar.name}
                        </h3>
                        <p className="text-sm text-blue-600 mt-1">
                          {avatar.experience}
                        </p>
                        <p className="text-sm text-gray-500 mt-1">
                          {avatar.description}
                        </p>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </>
      )}

      {/* Stats Section */}
      <div className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-400">700+</div>
              <div className="text-gray-400 mt-1">Episodes</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-400">7</div>
              <div className="text-gray-400 mt-1">Years</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-400">500+</div>
              <div className="text-gray-400 mt-1">Top Producers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-400">9</div>
              <div className="text-gray-400 mt-1">Problem Categories</div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>Keeping It Real Podcast by D.J. Paris</p>
            <p className="mt-1">VP of Business Development at Kale Realty, Chicago</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
