import Link from "next/link";
import { PROBLEM_CATEGORIES } from "@/lib/types";
import problemMap from "@/data/problem_episode_map.json";

export default function ProblemsPage() {
  const problemData = problemMap as Record<string, Record<string, unknown[]>>;

  // Count episodes per category
  const getCategoryCount = (category: string) => {
    const problems = problemData[category] || {};
    return Object.values(problems).reduce((sum, episodes) => sum + (episodes?.length || 0), 0);
  };

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-900">Browse by Problem</h1>
          <p className="text-gray-600 mt-2">
            Find episodes that address your specific challenges
          </p>
        </div>
      </div>

      {/* Categories Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(PROBLEM_CATEGORIES).map(([key, category]) => {
            const count = getCategoryCount(key);
            const problems = Object.keys(problemData[key] || {});

            return (
              <Link
                key={key}
                href={`/problems/${key}`}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-blue-300 transition group"
              >
                <div className="flex items-start justify-between mb-4">
                  <span className="text-4xl">{category.icon}</span>
                  {count > 0 && (
                    <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">
                      {count} episode{count !== 1 ? "s" : ""}
                    </span>
                  )}
                </div>
                <h3 className="font-bold text-xl text-gray-900 group-hover:text-blue-600 transition mb-2">
                  {category.name}
                </h3>
                <p className="text-gray-500 mb-4">{category.description}</p>

                {problems.length > 0 && (
                  <div className="border-t border-gray-100 pt-4">
                    <p className="text-sm text-gray-500 mb-2">Problems addressed:</p>
                    <ul className="space-y-1">
                      {problems.slice(0, 3).map((problem, idx) => (
                        <li key={idx} className="text-sm text-gray-600 flex items-center gap-2">
                          <span className="text-blue-500">•</span>
                          {problem}
                        </li>
                      ))}
                      {problems.length > 3 && (
                        <li className="text-sm text-gray-400">
                          +{problems.length - 3} more...
                        </li>
                      )}
                    </ul>
                  </div>
                )}

                {problems.length === 0 && (
                  <p className="text-sm text-gray-400 italic">
                    Episodes coming soon...
                  </p>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </main>
  );
}
