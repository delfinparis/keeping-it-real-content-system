"use client";

import Link from "next/link";
import allAnalysis from "@/data/all_analysis.json";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

interface AnalysisData {
  guest_info?: {
    name?: string | null;
    title?: string | null;
    company?: string | null;
    production_level?: string | null;
    specialty?: string | null;
  };
  main_topics?: string[];
  problems_addressed?: Array<{
    category: string;
    specific_problem: string;
    solution_summary: string;
  }>;
  clip_worthy_moments?: Array<{
    quote: string;
    clip_type: string;
    suggested_hook: string;
  }>;
  key_tactics?: Array<{
    tactic: string;
  }>;
  quotable_insights?: string[];
}

const analysisData = allAnalysis as Record<string, AnalysisData>;

// Calculate insights
function calculateInsights() {
  const categoryCount: Record<string, number> = {};
  const problemCount: Record<string, number> = {};
  const clipTypeCount: Record<string, number> = {};
  const topicCount: Record<string, number> = {};
  const tacticCount: Record<string, number> = {};

  let totalClips = 0;
  let totalProblems = 0;
  let totalTactics = 0;
  let totalQuotes = 0;

  const topGuests: Array<{ name: string; title: string; problems: number; clips: number }> = [];

  for (const [id, data] of Object.entries(analysisData)) {
    const guestProblems = data.problems_addressed?.length || 0;
    const guestClips = data.clip_worthy_moments?.length || 0;

    if (data.guest_info?.name) {
      topGuests.push({
        name: data.guest_info.name,
        title: data.guest_info.title || "",
        problems: guestProblems,
        clips: guestClips,
      });
    }

    // Count problems by category
    data.problems_addressed?.forEach((p) => {
      categoryCount[p.category] = (categoryCount[p.category] || 0) + 1;
      const key = `${p.category}:${p.specific_problem}`;
      problemCount[key] = (problemCount[key] || 0) + 1;
      totalProblems++;
    });

    // Count clips by type
    data.clip_worthy_moments?.forEach((c) => {
      clipTypeCount[c.clip_type] = (clipTypeCount[c.clip_type] || 0) + 1;
      totalClips++;
    });

    // Count topics
    data.main_topics?.forEach((t) => {
      topicCount[t] = (topicCount[t] || 0) + 1;
    });

    // Count tactics
    data.key_tactics?.forEach((t) => {
      tacticCount[t.tactic] = (tacticCount[t.tactic] || 0) + 1;
      totalTactics++;
    });

    totalQuotes += data.quotable_insights?.length || 0;
  }

  // Sort and get top items
  const topCategories = Object.entries(categoryCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const topProblems = Object.entries(problemCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15);

  const topClipTypes = Object.entries(clipTypeCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);

  const topTopics = Object.entries(topicCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12);

  const sortedGuests = topGuests
    .sort((a, b) => b.clips + b.problems - (a.clips + a.problems))
    .slice(0, 10);

  return {
    totalEpisodes: Object.keys(analysisData).length,
    totalClips,
    totalProblems,
    totalTactics,
    totalQuotes,
    topCategories,
    topProblems,
    topClipTypes,
    topTopics,
    topGuests: sortedGuests,
  };
}

const CATEGORY_LABELS: Record<string, { label: string; icon: string; color: string }> = {
  lead_generation: { label: "Lead Generation", icon: "📈", color: "bg-blue-500" },
  personal_brand: { label: "Personal Brand", icon: "🎯", color: "bg-purple-500" },
  market_industry: { label: "Market & Industry", icon: "🏠", color: "bg-green-500" },
  mindset_motivation: { label: "Mindset", icon: "🧠", color: "bg-yellow-500" },
  systems_operations: { label: "Systems", icon: "⚙️", color: "bg-gray-500" },
  money_business: { label: "Business & Money", icon: "💰", color: "bg-emerald-500" },
  client_management: { label: "Client Management", icon: "🤝", color: "bg-indigo-500" },
  conversion_sales: { label: "Conversion & Sales", icon: "🎪", color: "bg-red-500" },
  time_productivity: { label: "Time & Productivity", icon: "⏰", color: "bg-orange-500" },
};

export default function InsightsPage() {
  const insights = calculateInsights();

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      {/* Page Header */}
      <div className="bg-gradient-kale text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-bold mb-2">Podcast Insights</h1>
          <p className="text-blue-100 text-lg">
            Analytics from {insights.totalEpisodes} analyzed episodes
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1">
        {/* Key Stats */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-12">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="text-3xl font-bold text-kale">{insights.totalEpisodes}</div>
            <div className="text-gray-500 text-sm mt-1">Episodes Analyzed</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="text-3xl font-bold text-purple-600">{insights.totalClips}</div>
            <div className="text-gray-500 text-sm mt-1">Clip-worthy Moments</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="text-3xl font-bold text-blue-600">{insights.totalProblems}</div>
            <div className="text-gray-500 text-sm mt-1">Problems Mapped</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="text-3xl font-bold text-green-600">{insights.totalTactics}</div>
            <div className="text-gray-500 text-sm mt-1">Tactics Extracted</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <div className="text-3xl font-bold text-orange-600">{insights.totalQuotes}</div>
            <div className="text-gray-500 text-sm mt-1">Quotable Insights</div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Top Problem Categories */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Top Problem Categories</h2>
            <div className="space-y-4">
              {insights.topCategories.map(([category, count]) => {
                const meta = CATEGORY_LABELS[category] || {
                  label: category,
                  icon: "📋",
                  color: "bg-gray-400",
                };
                const percentage = Math.round((count / insights.totalProblems) * 100);
                return (
                  <div key={category}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="flex items-center gap-2 text-sm font-medium text-gray-700">
                        <span>{meta.icon}</span>
                        {meta.label}
                      </span>
                      <span className="text-sm text-gray-500">{count} episodes</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2">
                      <div
                        className={`${meta.color} h-2 rounded-full transition-all`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Clip Types */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Content Types</h2>
            <div className="grid grid-cols-2 gap-4">
              {insights.topClipTypes.map(([type, count]) => (
                <div
                  key={type}
                  className="bg-gray-50 rounded-lg p-4 border border-gray-100"
                >
                  <div className="text-2xl font-bold text-kale">{count}</div>
                  <div className="text-sm text-gray-600 capitalize">
                    {type.replace(/_/g, " ")}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Top Specific Problems */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 md:col-span-2">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Most Common Specific Problems</h2>
            <div className="grid md:grid-cols-3 gap-3">
              {insights.topProblems.map(([problem, count], idx) => {
                const [category, specific] = problem.split(":");
                const meta = CATEGORY_LABELS[category] || { icon: "📋" };
                return (
                  <div
                    key={problem}
                    className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg border border-gray-100"
                  >
                    <span className="text-lg">{meta.icon}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 leading-tight">
                        {specific}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">{count} episodes</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Top Topics */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Trending Topics</h2>
            <div className="flex flex-wrap gap-2">
              {insights.topTopics.map(([topic, count]) => (
                <span
                  key={topic}
                  className="px-3 py-1.5 bg-kale-50 text-kale rounded-full text-sm font-medium"
                >
                  {topic} ({count})
                </span>
              ))}
            </div>
          </div>

          {/* Top Guests */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Most Insightful Guests</h2>
            <div className="space-y-3">
              {insights.topGuests.map((guest, idx) => (
                <div
                  key={guest.name}
                  className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
                >
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 bg-kale text-white rounded-full flex items-center justify-center text-xs font-bold">
                      {idx + 1}
                    </span>
                    <div>
                      <p className="font-medium text-gray-900">{guest.name}</p>
                      <p className="text-xs text-gray-500">{guest.title}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-kale">{guest.clips} clips</p>
                    <p className="text-xs text-gray-500">{guest.problems} problems</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-12 text-center">
          <Link
            href="/"
            className="inline-flex items-center gap-2 bg-kale text-white px-8 py-4 rounded-xl font-semibold hover:bg-kale-light transition"
          >
            <span>Find Episodes for Your Challenge</span>
            <span>→</span>
          </Link>
        </div>
      </div>

      <Footer />
    </main>
  );
}
