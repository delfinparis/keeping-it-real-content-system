"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { PROBLEM_CATEGORIES, AVATARS } from "@/lib/types";
import ProblemWizard from "@/components/ProblemWizard";

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

interface WizardSelection {
  step1: string | null;
  step2: string | null;
  step3: string | null;
  step4: string | null;
  step5: string;
}

export default function Home() {
  const [mode, setMode] = useState<"wizard" | "search" | "browse">("wizard");
  const [challenge, setChallenge] = useState("");
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);
  const [problemMap, setProblemMap] = useState<{ [key: string]: { [key: string]: any[] } }>({});
  const [wizardSelections, setWizardSelections] = useState<WizardSelection | null>(null);

  // Load problem map for wizard
  useEffect(() => {
    fetch("/api/problems")
      .then((res) => res.json())
      .then((data) => setProblemMap(data))
      .catch(console.error);
  }, []);

  const getRecommendations = async (searchChallenge?: string) => {
    const query = searchChallenge || challenge;
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ challenge: query }),
      });
      const data = await res.json();
      setRecommendations(data);
      setMode("search"); // Switch to results view
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleWizardComplete = (context: string, selections: WizardSelection) => {
    setChallenge(context);
    setWizardSelections(selections);
    getRecommendations(context);
  };

  const startOver = () => {
    setRecommendations(null);
    setChallenge("");
    setWizardSelections(null);
    setMode("wizard");
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

  // Show loading state
  if (loading) {
    return (
      <main className="min-h-screen bg-gradient-kale flex items-center justify-center">
        <div className="text-center text-white">
          <div className="w-20 h-20 border-4 border-white border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
          <h2 className="text-2xl font-bold mb-2">Finding the perfect episodes...</h2>
          <p className="text-gray-300">Analyzing 700+ episodes to match this challenge</p>
        </div>
      </main>
    );
  }

  // Show recommendations
  if (recommendations && recommendations.recommendations?.length > 0) {
    return (
      <main className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-gradient-kale text-white py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <button
              onClick={startOver}
              className="text-blue-200 hover:text-white mb-4 flex items-center space-x-1 transition"
            >
              <span>←</span>
              <span>Start New Search</span>
            </button>
            <h1 className="text-3xl font-bold">Your Episode Recommendations</h1>
            <p className="text-blue-200 mt-2">{recommendations.summary}</p>
          </div>
        </div>

        {/* Results */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              Top {recommendations.recommendations.length} Episodes
            </h2>
            <button
              onClick={copyAllLinks}
              className="bg-kale text-white px-6 py-3 rounded-lg font-medium hover:bg-kale-light transition flex items-center space-x-2"
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
                      <div className="bg-kale text-white w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg">
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
                            <span className="bg-kale text-white px-3 py-1 rounded-lg text-sm font-mono font-bold whitespace-nowrap">
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

                  {/* Episode Link */}
                  <div className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-gray-500 mb-1">Episode Link:</p>
                        <p className="text-kale font-mono text-sm truncate">{rec.episode_url}</p>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => copyLink(rec.episode_url, rec.episode_id)}
                          className={`px-6 py-3 rounded-lg font-medium transition flex items-center space-x-2 ${
                            copied === rec.episode_id
                              ? "bg-green-600 text-white"
                              : "bg-kale text-white hover:bg-kale-light"
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
                              <span>Copy</span>
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

          {/* Message Template */}
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
                  : "bg-kale text-white hover:bg-kale-light"
              }`}
            >
              {copied === "template" ? "✓ Copied Template!" : "📋 Copy Full Message"}
            </button>
          </div>
        </div>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-12">
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

  // Show wizard or browse mode
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-kale text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 text-center">
            Find the Perfect Episode
          </h1>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto text-center">
            700+ episodes of top producer wisdom. Let's find exactly what your agent needs.
          </p>

          {/* Mode Toggle */}
          <div className="flex justify-center space-x-2 mb-8">
            <button
              onClick={() => setMode("wizard")}
              className={`px-6 py-3 rounded-lg font-medium transition ${
                mode === "wizard"
                  ? "bg-white text-kale"
                  : "bg-blue-700 text-white hover:bg-kale"
              }`}
            >
              🎯 Guided Search
            </button>
            <button
              onClick={() => setMode("search")}
              className={`px-6 py-3 rounded-lg font-medium transition ${
                mode === "search"
                  ? "bg-white text-kale"
                  : "bg-blue-700 text-white hover:bg-kale"
              }`}
            >
              ✍️ Describe Directly
            </button>
            <button
              onClick={() => setMode("browse")}
              className={`px-6 py-3 rounded-lg font-medium transition ${
                mode === "browse"
                  ? "bg-white text-kale"
                  : "bg-blue-700 text-white hover:bg-kale"
              }`}
            >
              📂 Browse Categories
            </button>
          </div>
        </div>
      </div>

      {/* Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Wizard Mode */}
        {mode === "wizard" && (
          <ProblemWizard onComplete={handleWizardComplete} problemMap={problemMap} />
        )}

        {/* Direct Search Mode */}
        {mode === "search" && !recommendations && (
          <div className="max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Describe the Agent's Challenge
            </h2>
            <textarea
              placeholder="Example: 'They've been in the business for 3 years, doing about 10 deals a year, but can't seem to break through to the next level. They're working tons of hours but not seeing the results. Their main struggle is lead generation - they feel like their sphere is tapped out.'"
              value={challenge}
              onChange={(e) => setChallenge(e.target.value)}
              rows={6}
              className="w-full px-6 py-4 rounded-xl text-gray-900 text-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 resize-none transition"
            />
            <button
              onClick={() => getRecommendations()}
              disabled={!challenge.trim()}
              className="mt-4 w-full bg-kale text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-kale-light transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              🎯 Get Episode Recommendations
            </button>
          </div>
        )}

        {/* Browse Mode */}
        {mode === "browse" && (
          <>
            {/* Problem Categories */}
            <div className="mb-16">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Browse by Challenge Category
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
                        <h3 className="font-semibold text-gray-900 group-hover:text-kale transition">
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

            {/* Avatars */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Browse by Agent Type
              </h2>
              <p className="text-gray-600 mb-8">
                Get recommendations based on where the agent is in their career
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
                        <h3 className="font-semibold text-gray-900 group-hover:text-kale transition">
                          {avatar.name}
                        </h3>
                        <p className="text-sm text-kale mt-1">
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
          </>
        )}
      </div>

      {/* Stats Section */}
      <div className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-white">8M+</div>
              <div className="text-gray-400 mt-1">Downloads</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white">700+</div>
              <div className="text-gray-400 mt-1">Episodes</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white">7</div>
              <div className="text-gray-400 mt-1">Years</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white">500+</div>
              <div className="text-gray-400 mt-1">Top Producers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-white">389</div>
              <div className="text-gray-400 mt-1">Problems Solved</div>
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
