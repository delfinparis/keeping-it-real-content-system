"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import episodesData from "@/data/episodes.json";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const episodes = episodesData.episodes;

export default function EpisodesPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"date" | "guest">("date");
  const [filterYear, setFilterYear] = useState<string>("all");

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

      return matchesSearch && matchesYear;
    });

    if (sortBy === "date") {
      filtered.sort((a, b) => (b.publish_date || "").localeCompare(a.publish_date || ""));
    } else {
      filtered.sort((a, b) => (a.guest_name || "").localeCompare(b.guest_name || ""));
    }

    return filtered;
  }, [searchQuery, sortBy, filterYear]);

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      {/* Page Header */}
      <div className="bg-gradient-kale text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-3xl font-bold">All Episodes</h1>
          <p className="text-blue-200 mt-2">
            Browse all {episodes.length} episodes from 7 years of interviews
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search episodes, guests, or topics..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Year Filter */}
            <div>
              <select
                value={filterYear}
                onChange={(e) => setFilterYear(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Years</option>
                {years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>

            {/* Sort */}
            <div>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "date" | "guest")}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="date">Sort by Date</option>
                <option value="guest">Sort by Guest</option>
              </select>
            </div>
          </div>
        </div>

        {/* Results count */}
        <p className="text-sm text-gray-500 mt-4">
          Showing {filteredEpisodes.length} of {episodes.length} episodes
        </p>
      </div>

      {/* Episode List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12 flex-1">
        <div className="space-y-4">
          {filteredEpisodes.map((episode) => (
            <div
              key={episode.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-kale/20 transition"
            >
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-sm text-gray-500">{episode.publish_date}</span>
                    {episode.duration_formatted && (
                      <span className="text-sm text-gray-500">⏱️ {episode.duration_formatted}</span>
                    )}
                  </div>
                  <h2 className="text-xl font-semibold text-gray-900 mb-1">
                    {episode.guest_name || "Unknown Guest"}
                  </h2>
                  <p className="text-gray-600 mb-3">{episode.title}</p>
                  <p className="text-gray-500 text-sm line-clamp-2">
                    {episode.description?.replace(/<[^>]*>/g, '').slice(0, 200)}...
                  </p>
                </div>
                <div className="flex flex-col sm:flex-row gap-2">
                  <Link
                    href={`/episodes/${episode.id}`}
                    className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition text-center"
                  >
                    View Details
                  </Link>
                  <a
                    href={episode.guid}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-kale text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-kale-light transition text-center"
                  >
                    🎧 Listen
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredEpisodes.length === 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <p className="text-gray-600 font-medium">No episodes found</p>
            <p className="text-gray-500 text-sm mt-1">Try adjusting your search or filters</p>
          </div>
        )}
      </div>

      <Footer />
    </main>
  );
}
