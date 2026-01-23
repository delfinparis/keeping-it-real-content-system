import Link from "next/link";
import { PROBLEM_CATEGORIES } from "@/lib/types";
import problemMap from "@/data/problem_episode_map.json";
import episodesData from "@/data/episodes.json";
const episodes = episodesData.episodes;

type Props = {
  params: Promise<{ category: string }>;
};

export default async function ProblemCategoryPage({ params }: Props) {
  const { category } = await params;
  const categoryInfo = PROBLEM_CATEGORIES[category];
  const problems = (problemMap as Record<string, Record<string, Array<{ episode: string; solution_summary: string; timestamp: string }>>>)[category] || {};

  // Get episode details helper
  const getEpisodeDetails = (episodeId: string) => {
    // episodeId format: "2026-01-05_item3_Tim-Burrell"
    const parts = episodeId.split("_");
    const guestName = parts[2]?.replace(/-/g, " ") || "Unknown Guest";
    const date = parts[0] || "";

    // Find in episodes array
    const found = episodes.find(
      (ep) => ep.guest_name?.toLowerCase().includes(guestName.toLowerCase().split(" ")[0])
    );

    return {
      guestName,
      date,
      title: found?.title || `Episode with ${guestName}`,
      duration: found?.duration_formatted || "",
      url: found?.guid || "#"
    };
  };

  if (!categoryInfo) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold text-gray-900">Category not found</h1>
        <Link href="/" className="text-blue-600 hover:underline mt-4 inline-block">
          Go back home
        </Link>
      </div>
    );
  }

  const problemEntries = Object.entries(problems);

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link href="/" className="text-blue-600 hover:underline text-sm mb-4 inline-block">
            ← Back to all categories
          </Link>
          <div className="flex items-center space-x-4">
            <span className="text-5xl">{categoryInfo.icon}</span>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{categoryInfo.name}</h1>
              <p className="text-gray-600 mt-1">{categoryInfo.description}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Problems List */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {problemEntries.length === 0 ? (
          <div className="bg-white rounded-xl p-8 text-center">
            <p className="text-gray-500">No episodes mapped to this category yet.</p>
            <p className="text-gray-400 text-sm mt-2">
              Episodes will appear here as more content is analyzed.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {problemEntries.map(([problem, episodesList]) => (
              <div key={problem} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                  <h2 className="font-semibold text-gray-900 text-lg">{problem}</h2>
                  <p className="text-sm text-gray-500">{episodesList.length} episode(s) address this</p>
                </div>
                <div className="divide-y divide-gray-100">
                  {episodesList.map((mapping, idx) => {
                    const details = getEpisodeDetails(mapping.episode);
                    return (
                      <div key={idx} className="p-6 hover:bg-gray-50 transition">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-medium text-gray-900">{details.guestName}</h3>
                            <p className="text-sm text-gray-500 mt-1">{details.title}</p>
                            <p className="text-gray-700 mt-3">{mapping.solution_summary}</p>
                            <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500">
                              <span>📍 Timestamp: {mapping.timestamp}</span>
                              {details.duration && <span>⏱️ {details.duration}</span>}
                            </div>
                          </div>
                          <div className="ml-4 flex flex-col space-y-2">
                            <a
                              href={details.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition text-center"
                            >
                              Listen
                            </a>
                            <button
                              onClick={() => {
                                navigator.clipboard.writeText(details.url);
                              }}
                              className="border border-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 transition"
                            >
                              Copy Link
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
