"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import episodesData from "@/data/episodes.json";
import Footer from "@/components/Footer";
import { useSavedEpisodes } from "@/hooks/useSavedEpisodes";

const episodes = episodesData.episodes;

// Get initials from guest name for avatar
function getInitials(name: string): string {
  if (!name) return "?";
  const parts = name.split(" ").filter(Boolean);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
}

// Generate a consistent color based on name
function getAvatarColor(name: string): string {
  const colors = [
    "bg-blue-500",
    "bg-green-500",
    "bg-purple-500",
    "bg-orange-500",
    "bg-pink-500",
    "bg-teal-500",
    "bg-indigo-500",
    "bg-red-500",
  ];
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
}

export default function EpisodesPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"date" | "guest">("date");
  const [filterYear, setFilterYear] = useState<string>("all");
  const [showSavedOnly, setShowSavedOnly] = useState(false);
  const { savedEpisodes, toggleSaved, isSaved, count: savedCount, isLoaded } = useSavedEpisodes();

  // Get unique years for filter
  const years = useMemo(() => {
    const yearSet = new Set(episodes.map(ep => ep.publish_date?.split("-")[0]).filter(Boolean));
    return Array.from(yearSet).sort().reverse();
  }, []);

  // Filter and sort episodes
  const filteredEpisodes = useMemo(() => {
    let filtered = episodes.filter(ep => {
      const matchesSearch = !searchQuery ||
        ep.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ep.guest_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ep.description?.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesYear = filterYear === "all" || ep.publish_date?.startsWith(filterYear);

      const matchesSaved = !showSavedOnly || savedEpisodes.includes(ep.id);

      return matchesSearch && matchesYear && matchesSaved;
    });

    if (sortBy === "date") {
      filtered.sort((a, b) => (b.publish_date || "").localeCompare(a.publish_date || ""));
    } else {
      filtered.sort((a, b) => (a.guest_name || "").localeCompare(b.guest_name || ""));
    }

    return filtered;
  }, [searchQuery, sortBy, filterYear, showSavedOnly, savedEpisodes]);

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">
      {/* Page Header */}
      <div className="bg-gradient-kale text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link
            href="/"
            className="text-blue-200 hover:text-white mb-4 flex items-center space-x-1 transition text-sm"
          >
            <span>←</span>
            <span>Back to Search</span>
          </Link>
          <h1 className="text-3xl font-bold">All Episodes</h1>
          <p className="text-blue-200 mt-2">
            Browse all {episodes.length} episodes from 7 years of interviews
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  placeholder="Search episodes, guests, or topics..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-kale/20 focus:border-kale"
                />
              </div>
            </div>

            {/* Filter Controls */}
            <div className="flex flex-wrap gap-2">
              {/* Year Filter */}
              <select
                value={filterYear}
                onChange={(e) => setFilterYear(e.target.value)}
                className="px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-kale/20 focus:border-kale bg-white"
              >
                <option value="all">All Years</option>
                {years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>

              {/* Sort */}
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "date" | "guest")}
                className="px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-kale/20 focus:border-kale bg-white"
              >
                <option value="date">Newest First</option>
                <option value="guest">A-Z by Guest</option>
              </select>

              {/* Saved Filter */}
              <button
                onClick={() => setShowSavedOnly(!showSavedOnly)}
                className={`px-4 py-2.5 rounded-lg font-medium transition flex items-center gap-2 ${
                  showSavedOnly
                    ? "bg-kale text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                <svg className="w-5 h-5" fill={showSavedOnly ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
                <span>Saved{isLoaded && savedCount > 0 ? ` (${savedCount})` : ""}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Results count */}
        <div className="flex items-center justify-between mt-4">
          <p className="text-sm text-gray-500">
            Showing {filteredEpisodes.length} of {episodes.length} episodes
          </p>
          {showSavedOnly && savedCount === 0 && (
            <p className="text-sm text-gray-500">
              No saved episodes yet. Click the bookmark icon to save episodes.
            </p>
          )}
        </div>
      </div>

      {/* Episode List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12 flex-1 w-full">
        <div className="space-y-4">
          {filteredEpisodes.map((episode) => (
            <div
              key={episode.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md hover:border-kale/20 transition"
            >
              <div className="flex gap-4">
                {/* Avatar */}
                <div
                  className={`w-14 h-14 rounded-full flex items-center justify-center text-white font-bold text-lg flex-shrink-0 ${getAvatarColor(
                    episode.guest_name || ""
                  )}`}
                >
                  {getInitials(episode.guest_name || "")}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-sm text-gray-500">{episode.publish_date}</span>
                        {episode.duration_formatted && (
                          <span className="text-sm text-gray-500">⏱️ {episode.duration_formatted}</span>
                        )}
                      </div>
                      <h2 className="text-xl font-semibold text-gray-900 mb-1">
                        {episode.guest_name || "Unknown Guest"}
                      </h2>
                      <p className="text-gray-600 mb-2 line-clamp-1">{episode.title}</p>
                      <p className="text-gray-500 text-sm line-clamp-2 hidden sm:block">
                        {episode.description?.replace(/<[^>]*>/g, '').slice(0, 200)}...
                      </p>
                    </div>

                    {/* Save Button */}
                    <button
                      onClick={() => toggleSaved(episode.id)}
                      className={`p-2 rounded-lg transition flex-shrink-0 ${
                        isSaved(episode.id)
                          ? "text-kale bg-kale/10"
                          : "text-gray-400 hover:text-kale hover:bg-gray-100"
                      }`}
                      title={isSaved(episode.id) ? "Remove from saved" : "Save episode"}
                    >
                      <svg className="w-6 h-6" fill={isSaved(episode.id) ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                      </svg>
                    </button>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-wrap gap-2 mt-3">
                    <Link
                      href={`/episodes/${episode.id}`}
                      className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
                    >
                      View Details
                    </Link>
                    <a
                      href={episode.guid}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-kale text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-kale-light transition"
                    >
                      🎧 Listen
                    </a>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredEpisodes.length === 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              {showSavedOnly ? (
                <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
              ) : (
                <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              )}
            </div>
            <p className="text-gray-600 font-medium">
              {showSavedOnly ? "No saved episodes" : "No episodes found"}
            </p>
            <p className="text-gray-500 text-sm mt-1">
              {showSavedOnly
                ? "Bookmark episodes to see them here"
                : "Try adjusting your search or filters"}
            </p>
            {showSavedOnly && (
              <button
                onClick={() => setShowSavedOnly(false)}
                className="mt-4 text-kale hover:underline text-sm font-medium"
              >
                View all episodes
              </button>
            )}
          </div>
        )}
      </div>

      <Footer />
    </main>
  );
}
