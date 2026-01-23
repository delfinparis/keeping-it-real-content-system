export interface Episode {
  item_number: number;
  title: string;
  guest_name: string;
  publish_date: string;
  duration: string;
  duration_seconds: number;
  description: string;
  mp3_url: string;
  episode_url: string;
}

export interface ProblemMapping {
  episode: string;
  solution_summary: string;
  timestamp: string;
}

export interface ProblemMap {
  [category: string]: {
    [problem: string]: ProblemMapping[];
  };
}

export interface AvatarMapping {
  episode: string;
  relevance: string;
  key_takeaway: string;
}

export interface AvatarMap {
  [avatarId: string]: AvatarMapping[];
}

export interface EpisodeAnalysis {
  guest_info: {
    name: string;
    title: string;
    company: string;
    production_level: string;
    specialty: string;
    location: string;
  };
  main_topics: string[];
  problems_addressed: {
    category: string;
    specific_problem: string;
    solution_summary: string;
    timestamp: string;
  }[];
  target_avatars: {
    avatar_id: string;
    relevance: string;
    key_takeaway: string;
  }[];
  clip_worthy_moments: {
    timestamp: string;
    end_timestamp: string;
    quote: string;
    clip_type: string;
    why_clipworthy: string;
    suggested_hook: string;
  }[];
  key_tactics: {
    tactic: string;
    context: string;
    timestamp: string;
  }[];
  quotable_insights: string[];
  resources_mentioned: {
    type: string;
    name: string;
    context: string;
  }[];
  episode_summary: string;
}

export const PROBLEM_CATEGORIES: { [key: string]: { name: string; icon: string; description: string } } = {
  lead_generation: {
    name: "Lead Generation",
    icon: "🎯",
    description: "Finding and attracting new clients"
  },
  conversion_sales: {
    name: "Conversion & Sales",
    icon: "💰",
    description: "Turning leads into closed deals"
  },
  time_productivity: {
    name: "Time & Productivity",
    icon: "⏰",
    description: "Working smarter, not harder"
  },
  systems_operations: {
    name: "Systems & Operations",
    icon: "⚙️",
    description: "Building a scalable business"
  },
  mindset_motivation: {
    name: "Mindset & Motivation",
    icon: "🧠",
    description: "Mental game and staying motivated"
  },
  money_business: {
    name: "Money & Business",
    icon: "📊",
    description: "Financial management and growth"
  },
  market_industry: {
    name: "Market & Industry",
    icon: "🏠",
    description: "Navigating market changes"
  },
  personal_brand: {
    name: "Personal Brand",
    icon: "✨",
    description: "Marketing yourself effectively"
  },
  client_management: {
    name: "Client Management",
    icon: "🤝",
    description: "Working with clients effectively"
  }
};

export const AVATARS: { [key: string]: { name: string; icon: string; experience: string; description: string } } = {
  overwhelmed_newbie: {
    name: "The Overwhelmed Newbie",
    icon: "🌱",
    experience: "0-2 years, 0-5 deals",
    description: "Just getting started, needs foundational guidance"
  },
  stuck_intermediate: {
    name: "The Stuck Intermediate",
    icon: "🔄",
    experience: "2-5 years, 6-15 deals",
    description: "Inconsistent results, looking for systems"
  },
  forgotten_middle: {
    name: "The Forgotten Middle",
    icon: "📈",
    experience: "5-10 years, 12-24 deals",
    description: "Plateaued, ready for the next level"
  },
  aspiring_top_producer: {
    name: "The Aspiring Top Producer",
    icon: "🚀",
    experience: "Any tenure, 25-50 deals",
    description: "Ready to scale and build leverage"
  },
  burned_out_veteran: {
    name: "The Burned-Out Veteran",
    icon: "🔥",
    experience: "10+ years, variable",
    description: "Needs renewal and better boundaries"
  },
  team_leader: {
    name: "The Team Leader",
    icon: "👥",
    experience: "Various",
    description: "Building and managing a team"
  }
};
