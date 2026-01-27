"use client";

import Link from "next/link";
import episodesData from "@/data/episodes.json";

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

export default function RecentEpisodes() {
  // Get the 6 most recent episodes
  const recentEpisodes = [...episodes]
    .sort((a, b) => (b.publish_date || "").localeCompare(a.publish_date || ""))
    .slice(0, 6);

  return (
    <div className="mb-12">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Recently Added</h2>
          <p className="text-gray-600 text-sm mt-1">Fresh insights from top producers</p>
        </div>
        <Link
          href="/episodes"
          className="text-kale hover:text-kale-light font-medium text-sm flex items-center gap-1 transition"
        >
          <span>View all episodes</span>
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {recentEpisodes.map((episode) => (
          <Link
            key={episode.id}
            href={`/episodes/${episode.id}`}
            className="bg-white rounded-xl p-4 shadow-sm border border-gray-200 hover:shadow-md hover:border-kale/30 transition group"
          >
            <div className="flex items-start gap-3">
              {/* Avatar */}
              <div
                className={`w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0 ${getAvatarColor(
                  episode.guest_name || ""
                )}`}
              >
                {getInitials(episode.guest_name || "")}
              </div>

              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-gray-900 group-hover:text-kale transition truncate">
                  {episode.guest_name || "Unknown Guest"}
                </h3>
                <p className="text-gray-500 text-sm truncate">{episode.title}</p>
                <div className="flex items-center gap-2 mt-2 text-xs text-gray-400">
                  <span>{episode.publish_date}</span>
                  {episode.duration_formatted && (
                    <>
                      <span>·</span>
                      <span>{episode.duration_formatted}</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
