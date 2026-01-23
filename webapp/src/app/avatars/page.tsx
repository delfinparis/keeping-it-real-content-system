import Link from "next/link";
import { AVATARS } from "@/lib/types";
import avatarMap from "@/data/avatar_episode_map.json";

const AVATAR_CHALLENGES: Record<string, string[]> = {
  overwhelmed_newbie: [
    "Just got licensed, doesn't know where to start",
    "No sphere of influence",
    "Afraid to pick up the phone",
    "Imposter syndrome"
  ],
  stuck_intermediate: [
    "Feast or famine production",
    "No systems",
    "Working too many hours",
    "Considering quitting"
  ],
  forgotten_middle: [
    "Plateaued production",
    "Missing out on tech/AI",
    "Tired of the hamster wheel",
    "Lacks accountability"
  ],
  aspiring_top_producer: [
    "Ready for next level",
    "Needs systems and leverage",
    "Considering building a team",
    "Looking for competitive edge"
  ],
  burned_out_veteran: [
    "Exhausted by constant change",
    "Technology overwhelm",
    "Considering leaving",
    "Needs passion renewal"
  ],
  team_leader: [
    "Hiring/managing challenges",
    "Compensation questions",
    "Lead distribution problems",
    "Culture and retention"
  ]
};

export default function AvatarsPage() {
  const avatarData = avatarMap as Record<string, unknown[]>;

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-blue-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-3xl md:text-4xl font-bold">Who Are You?</h1>
          <p className="text-blue-100 mt-2 text-lg">
            Get personalized episode recommendations based on where you are in your career
          </p>
        </div>
      </div>

      {/* Avatars Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(AVATARS).map(([key, avatar]) => {
            const episodeCount = avatarData[key]?.length || 0;
            const challenges = AVATAR_CHALLENGES[key] || [];

            return (
              <Link
                key={key}
                href={`/avatars/${key}`}
                className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg hover:border-blue-300 transition group"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-4">
                      <span className="text-5xl">{avatar.icon}</span>
                      <div>
                        <h3 className="font-bold text-xl text-gray-900 group-hover:text-blue-600 transition">
                          {avatar.name}
                        </h3>
                        <p className="text-blue-600 font-medium">{avatar.experience}</p>
                      </div>
                    </div>
                    {episodeCount > 0 && (
                      <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
                        {episodeCount} episode{episodeCount !== 1 ? "s" : ""}
                      </span>
                    )}
                  </div>

                  <p className="text-gray-600 mb-4">{avatar.description}</p>

                  <div className="border-t border-gray-100 pt-4">
                    <p className="text-sm font-medium text-gray-500 mb-2">Common Challenges:</p>
                    <div className="flex flex-wrap gap-2">
                      {challenges.slice(0, 4).map((challenge, idx) => (
                        <span
                          key={idx}
                          className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm"
                        >
                          {challenge}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
                  <span className="text-blue-600 font-medium group-hover:text-blue-700 transition">
                    View recommended episodes →
                  </span>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* How to Use */}
      <div className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">How to Use This</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 text-blue-600 w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Identify the Avatar</h3>
              <p className="text-gray-600 text-sm">
                During your conversation, determine which avatar best matches the agent's situation
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 text-blue-600 w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Find Relevant Episodes</h3>
              <p className="text-gray-600 text-sm">
                Click on the avatar to see curated episodes with specific timestamps and takeaways
              </p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 text-blue-600 w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Send as Value-Add</h3>
              <p className="text-gray-600 text-sm">
                Copy the links and send them to the agent as a value-add before any recruiting pitch
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
