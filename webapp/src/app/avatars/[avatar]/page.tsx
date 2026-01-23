"use client";

import { use, useState } from "react";
import Link from "next/link";
import { AVATARS } from "@/lib/types";
import avatarMap from "@/data/avatar_episode_map.json";
import episodesData from "@/data/episodes.json";

const episodes = episodesData.episodes;

const AVATAR_CHALLENGES: Record<string, string[]> = {
  overwhelmed_newbie: [
    "Just got licensed, doesn't know where to start",
    "No sphere of influence or it's tapped out",
    "Afraid to pick up the phone",
    "Doesn't understand the transaction process",
    "Imposter syndrome",
    "Burning through savings waiting for first deal"
  ],
  stuck_intermediate: [
    "Knows enough to be dangerous but not enough to scale",
    "Inconsistent production (feast or famine)",
    "No systems, everything is manual",
    "Working too many hours for too little return",
    "Can't figure out lead generation that works",
    "Considering quitting"
  ],
  forgotten_middle: [
    "Decent production but plateaued",
    "Not getting attention from brokerage leadership",
    "Missing out on tech/AI revolution",
    "Tired of the hamster wheel",
    "Wants mentorship but too experienced for newbie training",
    "Knows they should do more but lacks accountability"
  ],
  aspiring_top_producer: [
    "Ready to break through to the next level",
    "Needs systems and leverage",
    "Considering building a team",
    "Wants coaching/mastermind community",
    "Looking for edge in competitive market",
    "Hungry but needs direction"
  ],
  burned_out_veteran: [
    "Has seen every market cycle",
    "Exhausted by constant change",
    "Clients expect 24/7 availability",
    "Technology feels overwhelming",
    "Considering leaving the business",
    "Needs to rediscover why they started"
  ],
  team_leader: [
    "Wants to scale beyond solo production",
    "Hiring/firing/managing people challenges",
    "Compensation structure questions",
    "Lead distribution problems",
    "Culture and retention issues"
  ]
};

type Props = {
  params: Promise<{ avatar: string }>;
};

export default function AvatarPage({ params }: Props) {
  const { avatar } = use(params);
  const avatarInfo = AVATARS[avatar];
  const avatarEpisodes = (avatarMap as Record<string, Array<{ episode: string; relevance: string; key_takeaway: string }>>)[avatar] || [];
  const challenges = AVATAR_CHALLENGES[avatar] || [];
  const [copied, setCopied] = useState<string | null>(null);

  if (!avatarInfo) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h1 className="text-2xl font-bold text-gray-900">Avatar not found</h1>
        <Link href="/" className="text-blue-600 hover:underline mt-4 inline-block">
          Go back home
        </Link>
      </div>
    );
  }

  const getEpisodeDetails = (episodeId: string) => {
    const parts = episodeId.split("_");
    const guestName = parts[2]?.replace(/-/g, " ") || "Unknown Guest";

    const found = episodes.find(
      (ep) => ep.guest_name?.toLowerCase().includes(guestName.toLowerCase().split(" ")[0])
    );

    return {
      guestName,
      title: found?.title || `Episode with ${guestName}`,
      duration: found?.duration_formatted || "",
      url: found?.guid || "#",
      id: found?.id
    };
  };

  const copyLink = async (url: string, id: string) => {
    await navigator.clipboard.writeText(url);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-blue-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <Link href="/" className="text-blue-200 hover:text-white text-sm mb-4 inline-block">
            ← Back to home
          </Link>
          <div className="flex items-center space-x-4">
            <span className="text-6xl">{avatarInfo.icon}</span>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold">{avatarInfo.name}</h1>
              <p className="text-blue-200 text-lg mt-1">{avatarInfo.experience}</p>
              <p className="text-blue-100 mt-2">{avatarInfo.description}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Recommended Episodes */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                <h2 className="text-xl font-bold text-gray-900">
                  Recommended Episodes for {avatarInfo.name}
                </h2>
                <p className="text-gray-500 text-sm mt-1">
                  {avatarEpisodes.length} episode(s) specifically curated for this stage
                </p>
              </div>

              {avatarEpisodes.length === 0 ? (
                <div className="p-8 text-center">
                  <p className="text-gray-500">No episodes mapped to this avatar yet.</p>
                  <p className="text-gray-400 text-sm mt-2">
                    Episodes will appear here as more content is analyzed.
                  </p>
                </div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {avatarEpisodes.map((mapping, idx) => {
                    const details = getEpisodeDetails(mapping.episode);
                    return (
                      <div key={idx} className="p-6 hover:bg-gray-50 transition">
                        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 text-lg">{details.guestName}</h3>
                            <p className="text-gray-600 text-sm">{details.title}</p>

                            <div className="mt-3 space-y-2">
                              <div>
                                <span className="text-sm font-medium text-gray-700">Why it's relevant:</span>
                                <p className="text-gray-600 text-sm">{mapping.relevance}</p>
                              </div>
                              <div>
                                <span className="text-sm font-medium text-gray-700">Key takeaway:</span>
                                <p className="text-gray-600 text-sm">{mapping.key_takeaway}</p>
                              </div>
                            </div>

                            {details.duration && (
                              <p className="text-gray-500 text-sm mt-2">⏱️ {details.duration}</p>
                            )}
                          </div>
                          <div className="flex flex-col gap-2">
                            {details.id && (
                              <Link
                                href={`/episodes/${details.id}`}
                                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition text-center"
                              >
                                View Details
                              </Link>
                            )}
                            <button
                              onClick={() => copyLink(details.url, mapping.episode)}
                              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                                copied === mapping.episode
                                  ? "bg-green-600 text-white"
                                  : "bg-blue-600 text-white hover:bg-blue-700"
                              }`}
                            >
                              {copied === mapping.episode ? "✓ Copied!" : "📋 Copy Link"}
                            </button>
                            <a
                              href={details.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="bg-gray-800 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-900 transition text-center"
                            >
                              🎧 Listen
                            </a>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Common Challenges */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4">Common Challenges</h3>
              <ul className="space-y-3">
                {challenges.map((challenge, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-red-500">•</span>
                    <span className="text-gray-700 text-sm">{challenge}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Quick Message */}
            <div className="bg-blue-50 rounded-xl border border-blue-200 p-6">
              <h3 className="font-bold text-blue-900 mb-3">Quick Recruitment Message</h3>
              <p className="text-blue-800 text-sm mb-4">
                Copy this message to send to agents who fit this profile:
              </p>
              <div className="bg-white rounded-lg p-4 text-sm text-gray-700 border border-blue-200">
                <p>Hey! Based on where you are in your career, I think you'd really benefit from these podcast episodes I've done with top producers who were in a similar situation:</p>
                <br />
                {avatarEpisodes.slice(0, 3).map((mapping, idx) => {
                  const details = getEpisodeDetails(mapping.episode);
                  return (
                    <p key={idx}>
                      {idx + 1}. {details.guestName}: {mapping.key_takeaway}
                    </p>
                  );
                })}
                <br />
                <p>Let me know if you'd like the links!</p>
              </div>
              <button
                onClick={async () => {
                  const message = `Hey! Based on where you are in your career, I think you'd really benefit from these podcast episodes I've done with top producers who were in a similar situation:\n\n${avatarEpisodes.slice(0, 3).map((mapping, idx) => {
                    const details = getEpisodeDetails(mapping.episode);
                    return `${idx + 1}. ${details.guestName}: ${mapping.key_takeaway}`;
                  }).join('\n')}\n\nLet me know if you'd like the links!`;
                  await navigator.clipboard.writeText(message);
                  setCopied("message");
                  setTimeout(() => setCopied(null), 2000);
                }}
                className={`mt-4 w-full px-4 py-2 rounded-lg font-medium transition ${
                  copied === "message"
                    ? "bg-green-600 text-white"
                    : "bg-blue-600 text-white hover:bg-blue-700"
                }`}
              >
                {copied === "message" ? "✓ Copied!" : "📋 Copy Message"}
              </button>
            </div>

            {/* Other Avatars */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4">Other Agent Types</h3>
              <div className="space-y-2">
                {Object.entries(AVATARS)
                  .filter(([key]) => key !== avatar)
                  .map(([key, av]) => (
                    <Link
                      key={key}
                      href={`/avatars/${key}`}
                      className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-50 transition"
                    >
                      <span>{av.icon}</span>
                      <span className="text-gray-700 text-sm">{av.name}</span>
                    </Link>
                  ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
