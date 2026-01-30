"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { PROBLEM_CATEGORIES, AVATARS } from "@/lib/types";
import ProblemWizard from "@/components/ProblemWizard";
import Footer from "@/components/Footer";
import RecentEpisodes from "@/components/RecentEpisodes";

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
  customContext: string;
}

export default function Home() {
  const [mode, setMode] = useState<"wizard" | "search" | "browse">("wizard");
  const [challenge, setChallenge] = useState("");
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState<string | null>(null);
  const [wizardSelections, setWizardSelections] = useState<WizardSelection | null>(null);

  const getRecommendations = async (searchChallenge?: string) => {
    const query = searchChallenge || challenge;
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ challenge: query }),
      });
      if (!res.ok) {
        throw new Error("Failed to get recommendations");
      }
      const data = await res.json();
      setRecommendations(data);
      setMode("search"); // Switch to results view
    } catch (err) {
      console.error("Error:", err);
      setError("Something went wrong. Please try again.");
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
    setError(null);
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

  // Show loading state with skeleton
  if (loading) {
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
              <span>Cancel Search</span>
            </button>
            <h1 className="text-3xl font-bold">Finding the Perfect Episodes...</h1>
            <p className="text-blue-200 mt-2">Analyzing 700+ episodes to match your challenge</p>
          </div>
        </div>

        {/* Skeleton Results */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center mb-8">
            <div className="w-12 h-12 border-4 border-kale border-t-transparent rounded-full animate-spin"></div>
          </div>
          <div className="space-y-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden animate-pulse">
                <div className="bg-gray-100 px-6 py-4 border-b border-gray-200">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-4">
                      <div className="bg-gray-300 w-10 h-10 rounded-full"></div>
                      <div>
                        <div className="h-5 bg-gray-300 rounded w-48 mb-2"></div>
                        <div className="h-3 bg-gray-200 rounded w-32"></div>
                      </div>
                    </div>
                    <div className="h-6 bg-gray-200 rounded-full w-24"></div>
                  </div>
                </div>
                <div className="p-6 space-y-4">
                  <div className="h-4 bg-gray-200 rounded w-full"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                  <div className="h-4 bg-gray-200 rounded w-4/6"></div>
                  <div className="h-20 bg-gray-100 rounded-lg mt-4"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
        <Footer />
      </main>
    );
  }

  // Show error state
  if (error) {
    return (
      <main className="min-h-screen bg-gray-50">
                <div className="max-w-2xl mx-auto px-4 py-20 text-center">
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Oops, something went wrong</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <button
                onClick={() => getRecommendations()}
                className="btn-primary"
              >
                Try Again
              </button>
              <button
                onClick={startOver}
                className="btn-secondary"
              >
                Start Over
              </button>
            </div>
          </div>
        </div>
        <Footer />
      </main>
    );
  }

  // Show empty results
  if (recommendations && recommendations.recommendations?.length === 0) {
    return (
      <main className="min-h-screen bg-gray-50">
                <div className="max-w-2xl mx-auto px-4 py-20 text-center">
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-kale" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No exact matches found</h2>
            <p className="text-gray-600 mb-6">
              We couldn't find episodes that closely match your specific challenge.
              Try broadening your search or browse our categories.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <button
                onClick={startOver}
                className="btn-primary"
              >
                Try Different Search
              </button>
              <button
                onClick={() => { startOver(); setMode("browse"); }}
                className="btn-secondary"
              >
                Browse Categories
              </button>
            </div>
          </div>
        </div>
        <Footer />
      </main>
    );
  }

  // Show recommendations
  if (recommendations && recommendations.recommendations?.length > 0) {
    return (
      <main className="min-h-screen bg-gray-50 flex flex-col">
                {/* Page Header */}
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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              Top {recommendations.recommendations.length} Episodes
            </h2>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={copyAllLinks}
                className="bg-kale text-white px-4 py-2 sm:px-6 sm:py-3 rounded-lg font-medium hover:bg-kale-light transition flex items-center space-x-2 text-sm sm:text-base"
              >
                {copied === "all" ? (
                  <>
                    <span>✓</span>
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <span>📋</span>
                    <span>Copy All</span>
                  </>
                )}
              </button>
              <button
                onClick={async () => {
                  const episodeIds = recommendations.recommendations.map((r) => r.episode_id).join(",");
                  const shareUrl = `${window.location.origin}/share?episodes=${episodeIds}&challenge=${encodeURIComponent(challenge)}`;
                  await navigator.clipboard.writeText(shareUrl);
                  setCopied("share-link");
                  setTimeout(() => setCopied(null), 2000);
                }}
                className="bg-gray-100 text-gray-700 px-4 py-2 sm:px-6 sm:py-3 rounded-lg font-medium hover:bg-gray-200 transition flex items-center space-x-2 text-sm sm:text-base"
              >
                {copied === "share-link" ? (
                  <>
                    <span>✓</span>
                    <span>Link Copied!</span>
                  </>
                ) : (
                  <>
                    <span>🔗</span>
                    <span>Share</span>
                  </>
                )}
              </button>
              <a
                href={`mailto:?subject=${encodeURIComponent("Podcast Episodes for You")}&body=${encodeURIComponent(
                  `Hey!\n\nBased on your challenges, I found some episodes from my podcast that directly address this:\n\n${recommendations.recommendations.map((r, i) => `${i + 1}. ${r.guest_name} - ${r.why_relevant}\n   Listen here: ${r.episode_url}`).join('\n\n')}\n\nLet me know what you think after listening!`
                )}`}
                className="bg-gray-100 text-gray-700 px-4 py-2 sm:px-6 sm:py-3 rounded-lg font-medium hover:bg-gray-200 transition flex items-center space-x-2 text-sm sm:text-base"
              >
                <span>📧</span>
                <span className="hidden sm:inline">Email</span>
              </a>
            </div>
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

          {/* Message Template - More Prominent */}
          <div className="mt-8 bg-gradient-to-r from-kale to-kale-light rounded-2xl shadow-lg p-6 text-white">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
              <div>
                <h3 className="font-bold text-lg">Ready to share with your agent?</h3>
                <p className="text-blue-200 text-sm">Copy a pre-formatted message with all recommendations</p>
              </div>
              <button
                onClick={async () => {
                  const template = `Hey! Based on what you told me about your challenges, I found some episodes from my podcast that directly address this:\n\n${recommendations.recommendations.map((r, i) => `${i + 1}. ${r.guest_name} - ${r.why_relevant}\n   Listen here: ${r.episode_url}\n   Jump to: ${r.key_moments?.[0]?.timestamp || 'Start'} for the key insight`).join('\n\n')}\n\nLet me know what you think after listening!`;
                  await navigator.clipboard.writeText(template);
                  setCopied("template");
                  setTimeout(() => setCopied(null), 2000);
                }}
                className={`px-6 py-3 rounded-lg font-medium transition whitespace-nowrap ${
                  copied === "template"
                    ? "bg-green-500 text-white"
                    : "bg-white text-kale hover:bg-gray-100"
                }`}
              >
                {copied === "template" ? "✓ Copied!" : "📧 Copy Message Template"}
              </button>
            </div>
            <details className="group">
              <summary className="cursor-pointer text-blue-200 text-sm hover:text-white transition flex items-center gap-2">
                <span>Preview message</span>
                <svg className="w-4 h-4 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </summary>
              <div className="mt-4 bg-white/10 rounded-lg p-4 font-mono text-sm text-blue-100 whitespace-pre-wrap backdrop-blur-sm">
{`Hey! Based on what you told me about your challenges, I found some episodes from my podcast that directly address this:

${recommendations.recommendations.map((r, i) => `${i + 1}. ${r.guest_name} - ${r.why_relevant}
   Listen here: ${r.episode_url}
   Jump to: ${r.key_moments?.[0]?.timestamp || 'Start'} for the key insight`).join('\n\n')}

Let me know what you think after listening!`}
              </div>
            </details>
          </div>
        </div>

        <Footer />
      </main>
    );
  }

  // Show wizard or browse mode
  return (
    <main className="min-h-screen flex flex-col">
            {/* Hero Section */}
      <div className="bg-gradient-kale text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Podcast Logo */}
          <div className="flex justify-center mb-6">
            <Image
              src="/kir-logo.jpg"
              alt="Keeping It Real Podcast"
              width={120}
              height={120}
              className="rounded-2xl shadow-lg"
            />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 text-center">
            Where are you stuck?
          </h1>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto text-center">
            Your biggest real estate agent problems have already been solved.
          </p>

          {/* Mode Toggle - Mobile Optimized */}
          <div className="flex flex-col sm:flex-row justify-center gap-2 sm:space-x-2 mb-8">
            <button
              onClick={() => setMode("wizard")}
              className={`px-5 py-3 rounded-lg font-medium transition flex items-center justify-center gap-2 ${
                mode === "wizard"
                  ? "bg-white text-kale shadow-lg"
                  : "bg-white/10 text-white hover:bg-white/20"
              }`}
            >
              <span>🎯</span>
              <span>Guided Search</span>
            </button>
            <button
              onClick={() => setMode("search")}
              className={`px-5 py-3 rounded-lg font-medium transition flex items-center justify-center gap-2 ${
                mode === "search"
                  ? "bg-white text-kale shadow-lg"
                  : "bg-white/10 text-white hover:bg-white/20"
              }`}
            >
              <span>✍️</span>
              <span>Describe Directly</span>
            </button>
            <button
              onClick={() => setMode("browse")}
              className={`px-5 py-3 rounded-lg font-medium transition flex items-center justify-center gap-2 ${
                mode === "browse"
                  ? "bg-white text-kale shadow-lg"
                  : "bg-white/10 text-white hover:bg-white/20"
              }`}
            >
              <span>📂</span>
              <span>Browse Categories</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content Area */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-1">
        {/* Wizard Mode */}
        {mode === "wizard" && (
          <ProblemWizard
            onComplete={handleWizardComplete}
            onQuickSearch={() => setMode("search")}
          />
        )}

        {/* Direct Search Mode */}
        {mode === "search" && !recommendations && (
          <div className="max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Tell us what you're struggling with
            </h2>
            <textarea
              placeholder="Example: 'I've been in the business for 3 years, doing about 10 deals a year, but can't seem to break through to the next level. I'm working tons of hours but not seeing the results. My main struggle is lead generation - I feel like my sphere is tapped out.'"
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
              Get Unstuck
            </button>
          </div>
        )}

        {/* Recently Added - Show on wizard and search modes */}
        {(mode === "wizard" || mode === "search") && !recommendations && (
          <div className="mt-12 border-t border-gray-200 pt-12">
            <RecentEpisodes />
          </div>
        )}

        {/* Browse Mode */}
        {mode === "browse" && (
          <>
            {/* Quick Access to All Episodes */}
            <div className="mb-8">
              <Link
                href="/episodes"
                className="inline-flex items-center gap-2 bg-kale text-white px-6 py-3 rounded-xl font-medium hover:bg-kale-light transition"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span>Browse All 700+ Episodes</span>
              </Link>
            </div>

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
                Browse by Experience Level
              </h2>
              <p className="text-gray-600 mb-8">
                Get recommendations based on where you are in your career
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
      <div className="bg-gray-50 border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <p className="text-center text-gray-500 text-sm uppercase tracking-wider mb-8">Trusted by real estate professionals worldwide</p>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-6 text-center">
            <div className="p-4">
              <div className="text-3xl md:text-4xl font-bold text-kale">8M+</div>
              <div className="text-gray-500 mt-1 text-sm">Downloads</div>
            </div>
            <div className="p-4">
              <div className="text-3xl md:text-4xl font-bold text-kale">700+</div>
              <div className="text-gray-500 mt-1 text-sm">Episodes</div>
            </div>
            <div className="p-4">
              <div className="text-3xl md:text-4xl font-bold text-kale">7</div>
              <div className="text-gray-500 mt-1 text-sm">Years Running</div>
            </div>
            <div className="p-4">
              <div className="text-3xl md:text-4xl font-bold text-kale">500+</div>
              <div className="text-gray-500 mt-1 text-sm">Top Producers</div>
            </div>
            <div className="p-4 col-span-2 md:col-span-1">
              <div className="text-3xl md:text-4xl font-bold text-kale">287</div>
              <div className="text-gray-500 mt-1 text-sm">Episodes Analyzed</div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </main>
  );
}
