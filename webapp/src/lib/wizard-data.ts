// Problem Wizard Hierarchy - Choose Your Own Adventure Style
// Optimized 4-step funnel: Core Struggle → Focus Area → Root Cause → Context

export interface WizardOption {
  id: string;
  label: string;
  description: string;
  icon: string;
}

export interface WizardStep {
  id: string;
  title: string;
  subtitle: string;
  options: WizardOption[];
}

// Step 1: Core Struggle - The big picture question (NOW 5 OPTIONS)
export const STEP_1_CORE_STRUGGLES: WizardStep = {
  id: "core_struggle",
  title: "What's the #1 thing holding you back?",
  subtitle: "",
  options: [
    {
      id: "more_business",
      label: "Not enough opportunities",
      description: "Pipeline is dry, need more leads and prospects",
      icon: "📉"
    },
    {
      id: "close_more",
      label: "Not converting opportunities",
      description: "Have leads but can't get them to yes",
      icon: "🎯"
    },
    {
      id: "work_smarter",
      label: "Drowning in chaos",
      description: "No systems, poor time management, always reactive",
      icon: "🌊"
    },
    {
      id: "grow_personally",
      label: "Stuck in my head",
      description: "Fear, doubt, burnout, or lack of confidence",
      icon: "🧠"
    },
    {
      id: "team_growth",
      label: "Team or business scaling",
      description: "Hiring, delegation, building leverage",
      icon: "👥"
    }
  ]
};

// Step 2: Focus Areas - 3-4 clear options each (REDUCED FROM 5)
export const STEP_2_FOCUS_AREAS: { [key: string]: WizardStep } = {
  more_business: {
    id: "focus_area",
    title: "Where's the pipeline breaking down?",
    subtitle: "Pick the weak spot",
    options: [
      {
        id: "no_leads",
        label: "Can't find leads",
        description: "Don't know where to look or how to generate",
        icon: "🔍"
      },
      {
        id: "sphere_dead",
        label: "Sphere isn't producing",
        description: "Past clients and network aren't referring",
        icon: "👻"
      },
      {
        id: "marketing_weak",
        label: "Marketing isn't working",
        description: "Social media, content, open houses not converting",
        icon: "📱"
      },
      {
        id: "new_to_area",
        label: "New to the market",
        description: "Don't have connections or reputation yet",
        icon: "🆕"
      }
    ]
  },
  close_more: {
    id: "focus_area",
    title: "Where are deals dying?",
    subtitle: "Find the leak in the bucket",
    options: [
      {
        id: "listing_loss",
        label: "Losing listings",
        description: "Can't win the listing appointment or beat competition",
        icon: "📋"
      },
      {
        id: "buyer_issues",
        label: "Buyers won't commit",
        description: "Ghosting, endless looking, going with others",
        icon: "👻"
      },
      {
        id: "negotiation",
        label: "Deals fall apart",
        description: "Inspection, negotiation, or contract issues",
        icon: "💔"
      },
      {
        id: "follow_up",
        label: "Leads go cold",
        description: "No system to nurture and convert over time",
        icon: "❄️"
      }
    ]
  },
  work_smarter: {
    id: "focus_area",
    title: "What's causing the chaos?",
    subtitle: "Identify the root cause",
    options: [
      {
        id: "no_systems",
        label: "No systems",
        description: "Everything is manual, nothing is organized",
        icon: "🎪"
      },
      {
        id: "time_suck",
        label: "Time disappears",
        description: "Always busy, never productive",
        icon: "⏰"
      },
      {
        id: "tech_overwhelm",
        label: "Tech overwhelm",
        description: "Too many tools or don't know what to use",
        icon: "💻"
      },
      {
        id: "no_boundaries",
        label: "No work-life balance",
        description: "Can't unplug, always available, burning out",
        icon: "🔥"
      }
    ]
  },
  grow_personally: {
    id: "focus_area",
    title: "What's the mental block?",
    subtitle: "Get to the heart of it",
    options: [
      {
        id: "fear_block",
        label: "Fear holding them back",
        description: "Fear of rejection, failure, or putting themselves out there",
        icon: "😰"
      },
      {
        id: "confidence",
        label: "Confidence issues",
        description: "Imposter syndrome, comparing to others, self-doubt",
        icon: "🎭"
      },
      {
        id: "burnout",
        label: "Burned out or lost",
        description: "Lost motivation, considering quitting, exhausted",
        icon: "🔋"
      },
      {
        id: "direction",
        label: "Unclear direction",
        description: "Don't know what path to take or how to grow",
        icon: "🧭"
      }
    ]
  },
  team_growth: {
    id: "focus_area",
    title: "What's the team/scaling challenge?",
    subtitle: "Where's the friction?",
    options: [
      {
        id: "hiring",
        label: "Finding the right people",
        description: "Don't know who to hire or how to attract talent",
        icon: "🎯"
      },
      {
        id: "delegation",
        label: "Can't let go",
        description: "Control issues, trust problems, doing everything",
        icon: "🎮"
      },
      {
        id: "team_performance",
        label: "Team underperforming",
        description: "Managing, motivating, holding accountable",
        icon: "📊"
      },
      {
        id: "scaling_model",
        label: "What model to build",
        description: "Team vs solo, partnership, brokerage decisions",
        icon: "🏗️"
      }
    ]
  }
};

// Step 3: Root Causes - More specific (3-4 options, action-oriented)
export const STEP_3_ROOT_CAUSES: { [key: string]: WizardStep } = {
  // FINDING OPPORTUNITIES
  no_leads: {
    id: "root_cause",
    title: "Why aren't leads coming in?",
    subtitle: "What resonates most?",
    options: [
      { id: "dont_know_how", label: "Don't know where to start", description: "Overwhelmed by options", icon: "🤷" },
      { id: "tried_everything", label: "Nothing seems to work", description: "Tried stuff, no results", icon: "😤" },
      { id: "hate_prospecting", label: "Hate prospecting", description: "Cold outreach feels awful", icon: "😣" },
      { id: "no_time_leads", label: "No time for lead gen", description: "Too busy with current clients", icon: "⏰" }
    ]
  },
  sphere_dead: {
    id: "root_cause",
    title: "Why isn't the sphere producing?",
    subtitle: "What's the real issue?",
    options: [
      { id: "dont_ask", label: "Don't ask for referrals", description: "Feels awkward", icon: "🤐" },
      { id: "lost_touch", label: "Lost touch with people", description: "Haven't reached out", icon: "📭" },
      { id: "forgettable", label: "Not top of mind", description: "They forget about me", icon: "👻" },
      { id: "small_network", label: "Network is too small", description: "Don't know enough people", icon: "📉" }
    ]
  },
  marketing_weak: {
    id: "root_cause",
    title: "What's not working?",
    subtitle: "Pick the biggest gap",
    options: [
      { id: "no_content_ideas", label: "Don't know what to post", description: "No content strategy", icon: "💭" },
      { id: "hate_camera", label: "Hate being on camera", description: "Video is uncomfortable", icon: "📷" },
      { id: "no_engagement", label: "No one engages", description: "Posting but no response", icon: "🦗" },
      { id: "inconsistent", label: "Can't stay consistent", description: "Start and stop", icon: "📅" }
    ]
  },
  new_to_area: {
    id: "root_cause",
    title: "What's the biggest challenge?",
    subtitle: "Starting fresh is hard",
    options: [
      { id: "no_connections", label: "No connections", description: "Don't know anyone", icon: "🏝️" },
      { id: "no_reputation", label: "No reputation yet", description: "Nobody knows me", icon: "❓" },
      { id: "dont_know_market", label: "Don't know the market", description: "Need local expertise", icon: "🗺️" }
    ]
  },

  // CLOSING DEALS
  listing_loss: {
    id: "root_cause",
    title: "Where do listings slip away?",
    subtitle: "Find the moment it breaks",
    options: [
      { id: "cant_get_appt", label: "Can't get the appointment", description: "They won't meet with me", icon: "🚪" },
      { id: "lose_presentation", label: "Lose during presentation", description: "They choose someone else", icon: "🥈" },
      { id: "price_objection", label: "Price disagreements", description: "Can't align on value", icon: "💰" },
      { id: "commission_pushback", label: "Commission pushback", description: "They want lower fees", icon: "📉" }
    ]
  },
  buyer_issues: {
    id: "root_cause",
    title: "What happens with buyers?",
    subtitle: "Where do they slip away?",
    options: [
      { id: "endless_looking", label: "They look forever", description: "Won't pull the trigger", icon: "🔄" },
      { id: "buyers_ghost", label: "They ghost me", description: "Stop responding", icon: "👻" },
      { id: "lose_to_agent", label: "They go with someone else", description: "Can't build loyalty", icon: "💔" },
      { id: "market_fear", label: "Scared of the market", description: "Worried about rates/prices", icon: "😨" }
    ]
  },
  negotiation: {
    id: "root_cause",
    title: "Where do negotiations fail?",
    subtitle: "What's the pattern?",
    options: [
      { id: "multiple_offers", label: "Lose in multiple offers", description: "Keep getting outbid", icon: "📊" },
      { id: "inspection_issues", label: "Inspection kills deals", description: "Falls apart on repairs", icon: "🔍" },
      { id: "not_assertive", label: "Not assertive enough", description: "Give in too easily", icon: "🤷" },
      { id: "difficult_parties", label: "Difficult people", description: "Other side is unreasonable", icon: "😤" }
    ]
  },
  follow_up: {
    id: "root_cause",
    title: "Why does follow-up fail?",
    subtitle: "What's breaking down?",
    options: [
      { id: "no_system", label: "No system", description: "Leads fall through cracks", icon: "🕳️" },
      { id: "dont_know_say", label: "Don't know what to say", description: "Follow-up feels awkward", icon: "🤐" },
      { id: "avoid_calls", label: "Avoid making calls", description: "Procrastinate on outreach", icon: "😬" },
      { id: "too_many_leads", label: "Too many to manage", description: "Overwhelmed by volume", icon: "🌊" }
    ]
  },

  // WORKING SMARTER
  no_systems: {
    id: "root_cause",
    title: "What needs systematizing?",
    subtitle: "Where's the biggest mess?",
    options: [
      { id: "crm_mess", label: "CRM is a disaster", description: "No organized database", icon: "📊" },
      { id: "transaction_chaos", label: "Transactions are chaotic", description: "Balls getting dropped", icon: "🎪" },
      { id: "no_processes", label: "No repeatable processes", description: "Reinvent the wheel every time", icon: "🔄" }
    ]
  },
  time_suck: {
    id: "root_cause",
    title: "Where does time go?",
    subtitle: "Find the black hole",
    options: [
      { id: "always_reactive", label: "Always reactive", description: "Putting out fires", icon: "🔥" },
      { id: "cant_say_no", label: "Can't say no", description: "Take on too much", icon: "🙋" },
      { id: "no_routine", label: "No routine", description: "Every day is chaos", icon: "🎲" },
      { id: "distractions", label: "Constant distractions", description: "Can't focus", icon: "📱" }
    ]
  },
  tech_overwhelm: {
    id: "root_cause",
    title: "What's the tech struggle?",
    subtitle: "Where's the friction?",
    options: [
      { id: "too_many_tools", label: "Too many tools", description: "Don't know what to use", icon: "😵" },
      { id: "not_using", label: "Have tools, don't use them", description: "Paying for stuff I ignore", icon: "🧊" },
      { id: "ai_confused", label: "Confused about AI", description: "Don't know how to leverage it", icon: "🤖" }
    ]
  },
  no_boundaries: {
    id: "root_cause",
    title: "What's out of balance?",
    subtitle: "Where's the breakdown?",
    options: [
      { id: "always_on", label: "Always available", description: "Can't set client boundaries", icon: "📱" },
      { id: "cant_unplug", label: "Can't mentally unplug", description: "Always thinking about work", icon: "🧠" },
      { id: "relationships_suffer", label: "Relationships suffering", description: "Family/friends neglected", icon: "👨‍👩‍👧" }
    ]
  },

  // MINDSET/PERSONAL GROWTH
  fear_block: {
    id: "root_cause",
    title: "What's the fear?",
    subtitle: "Name it to tame it",
    options: [
      { id: "fear_rejection", label: "Fear of rejection", description: "Hate hearing no", icon: "😰" },
      { id: "fear_judgment", label: "Fear of judgment", description: "What will people think?", icon: "👀" },
      { id: "fear_failure", label: "Fear of failure", description: "What if I'm not good enough?", icon: "😨" },
      { id: "fear_visibility", label: "Fear of visibility", description: "Don't want to put myself out there", icon: "🙈" }
    ]
  },
  confidence: {
    id: "root_cause",
    title: "What's undermining confidence?",
    subtitle: "Get to the root",
    options: [
      { id: "imposter", label: "Imposter syndrome", description: "Feel like a fraud", icon: "🎭" },
      { id: "comparison", label: "Comparing to others", description: "Everyone seems ahead", icon: "📊" },
      { id: "negative_talk", label: "Negative self-talk", description: "Inner critic is loud", icon: "💬" },
      { id: "past_failures", label: "Past failures haunting", description: "Can't move past mistakes", icon: "👻" }
    ]
  },
  burnout: {
    id: "root_cause",
    title: "What's draining energy?",
    subtitle: "Find the leak",
    options: [
      { id: "lost_why", label: "Lost the 'why'", description: "Don't remember why I started", icon: "❓" },
      { id: "roller_coaster", label: "Income rollercoaster", description: "Feast or famine is exhausting", icon: "🎢" },
      { id: "considering_quit", label: "Thinking of quitting", description: "Is this even worth it?", icon: "🚪" },
      { id: "completely_empty", label: "Running on empty", description: "No energy left", icon: "🔋" }
    ]
  },
  direction: {
    id: "root_cause",
    title: "What's the direction question?",
    subtitle: "What decision is pending?",
    options: [
      { id: "team_vs_solo", label: "Team vs solo?", description: "Should I join or stay independent?", icon: "👥" },
      { id: "niche_down", label: "Should I specialize?", description: "Niche or stay general?", icon: "🎯" },
      { id: "switch_brokerages", label: "Switch brokerages?", description: "Is the grass greener?", icon: "🏠" }
    ]
  },

  // TEAM/SCALING
  hiring: {
    id: "root_cause",
    title: "What's the hiring challenge?",
    subtitle: "Where's it breaking down?",
    options: [
      { id: "who_to_hire", label: "Don't know who to hire first", description: "Admin? Buyer's agent? ISA?", icon: "🤔" },
      { id: "cant_attract", label: "Can't attract good people", description: "Nobody wants to join", icon: "🎣" },
      { id: "afford_help", label: "Can't afford help yet", description: "Chicken and egg problem", icon: "💸" }
    ]
  },
  delegation: {
    id: "root_cause",
    title: "Why is delegation hard?",
    subtitle: "What's the real block?",
    options: [
      { id: "trust_issues", label: "Trust issues", description: "They won't do it right", icon: "🔒" },
      { id: "faster_myself", label: "Faster to do it myself", description: "Training takes too long", icon: "⚡" },
      { id: "what_delegate", label: "Don't know what to delegate", description: "Unclear what to hand off", icon: "❓" }
    ]
  },
  team_performance: {
    id: "root_cause",
    title: "What's the team issue?",
    subtitle: "Where's the gap?",
    options: [
      { id: "accountability", label: "Accountability problems", description: "They don't deliver", icon: "📋" },
      { id: "motivation", label: "Motivation issues", description: "They're not driven", icon: "🔋" },
      { id: "training_gaps", label: "Training gaps", description: "They need more skills", icon: "📚" },
      { id: "wrong_people", label: "Wrong people", description: "Need to make changes", icon: "🔄" }
    ]
  },
  scaling_model: {
    id: "root_cause",
    title: "What's the scaling question?",
    subtitle: "What's the decision?",
    options: [
      { id: "build_team", label: "Should I build a team?", description: "Is it time?", icon: "👥" },
      { id: "what_structure", label: "What structure?", description: "Team model, split, etc.", icon: "🏗️" },
      { id: "expand_market", label: "Expand to new markets?", description: "Geographic growth", icon: "🗺️" }
    ]
  }
};

// Mapping from Step 3 root causes to actual problem categories
export const ROOT_CAUSE_TO_CATEGORIES: { [key: string]: string[] } = {
  // Finding opportunities
  dont_know_how: ["lead_generation"],
  tried_everything: ["lead_generation"],
  hate_prospecting: ["lead_generation", "mindset_motivation"],
  no_time_leads: ["lead_generation", "time_productivity"],

  dont_ask: ["lead_generation", "mindset_motivation"],
  lost_touch: ["lead_generation", "systems_operations"],
  forgettable: ["lead_generation", "personal_brand"],
  small_network: ["lead_generation"],

  no_content_ideas: ["personal_brand"],
  hate_camera: ["personal_brand", "mindset_motivation"],
  no_engagement: ["personal_brand"],
  inconsistent: ["personal_brand", "time_productivity"],

  no_connections: ["lead_generation"],
  no_reputation: ["lead_generation", "personal_brand"],
  dont_know_market: ["market_industry"],

  // Closing deals
  cant_get_appt: ["lead_generation", "conversion_sales"],
  lose_presentation: ["conversion_sales"],
  price_objection: ["conversion_sales"],
  commission_pushback: ["conversion_sales", "money_business"],

  endless_looking: ["conversion_sales"],
  buyers_ghost: ["conversion_sales", "client_management"],
  lose_to_agent: ["conversion_sales"],
  market_fear: ["conversion_sales", "market_industry"],

  multiple_offers: ["conversion_sales"],
  inspection_issues: ["conversion_sales"],
  not_assertive: ["conversion_sales", "mindset_motivation"],
  difficult_parties: ["conversion_sales"],

  no_system: ["systems_operations", "conversion_sales"],
  dont_know_say: ["conversion_sales"],
  avoid_calls: ["mindset_motivation", "conversion_sales"],
  too_many_leads: ["systems_operations"],

  // Working smarter
  crm_mess: ["systems_operations"],
  transaction_chaos: ["systems_operations"],
  no_processes: ["systems_operations"],

  always_reactive: ["time_productivity"],
  cant_say_no: ["time_productivity", "mindset_motivation"],
  no_routine: ["time_productivity"],
  distractions: ["time_productivity"],

  too_many_tools: ["systems_operations"],
  not_using: ["systems_operations"],
  ai_confused: ["systems_operations", "market_industry"],

  always_on: ["time_productivity", "client_management"],
  cant_unplug: ["mindset_motivation"],
  relationships_suffer: ["time_productivity"],

  // Mindset
  fear_rejection: ["mindset_motivation"],
  fear_judgment: ["mindset_motivation"],
  fear_failure: ["mindset_motivation"],
  fear_visibility: ["mindset_motivation", "personal_brand"],

  imposter: ["mindset_motivation"],
  comparison: ["mindset_motivation"],
  negative_talk: ["mindset_motivation"],
  past_failures: ["mindset_motivation"],

  lost_why: ["mindset_motivation"],
  roller_coaster: ["mindset_motivation", "money_business"],
  considering_quit: ["mindset_motivation"],
  completely_empty: ["mindset_motivation"],

  team_vs_solo: ["money_business", "systems_operations"],
  niche_down: ["personal_brand"],
  switch_brokerages: ["money_business"],

  // Team/Scaling
  who_to_hire: ["systems_operations"],
  cant_attract: ["systems_operations"],
  afford_help: ["money_business"],

  trust_issues: ["mindset_motivation", "systems_operations"],
  faster_myself: ["systems_operations"],
  what_delegate: ["systems_operations"],

  accountability: ["systems_operations"],
  motivation: ["systems_operations"],
  training_gaps: ["systems_operations"],
  wrong_people: ["systems_operations"],

  build_team: ["systems_operations", "money_business"],
  what_structure: ["systems_operations"],
  expand_market: ["market_industry"]
};

// Simplified keyword matching
export const ROOT_CAUSE_KEYWORDS: { [key: string]: string[] } = {
  dont_know_how: ["start", "begin", "new", "where"],
  tried_everything: ["tried", "nothing", "work"],
  hate_prospecting: ["cold", "call", "prospect"],
  no_time_leads: ["time", "busy"],

  dont_ask: ["ask", "referral"],
  lost_touch: ["touch", "contact", "reach"],
  forgettable: ["remember", "top of mind", "forget"],
  small_network: ["small", "network", "sphere"],

  no_content_ideas: ["content", "post", "idea"],
  hate_camera: ["camera", "video"],
  no_engagement: ["engage", "like", "comment"],
  inconsistent: ["consistent", "regular"],

  cant_get_appt: ["appointment", "meet"],
  lose_presentation: ["presentation", "listing", "compete"],
  price_objection: ["price", "value"],
  commission_pushback: ["commission", "fee"],

  endless_looking: ["commit", "decide", "looking"],
  buyers_ghost: ["ghost", "respond"],
  lose_to_agent: ["other agent", "loyalty"],
  market_fear: ["rate", "market", "afraid"],

  multiple_offers: ["multiple", "offer", "outbid"],
  inspection_issues: ["inspection", "repair"],
  not_assertive: ["assertive", "push"],

  no_system: ["system", "crm", "track"],
  dont_know_say: ["say", "script"],
  avoid_calls: ["call", "phone", "avoid"],

  crm_mess: ["crm", "database"],
  transaction_chaos: ["transaction", "deal"],

  always_reactive: ["reactive", "fire"],
  cant_say_no: ["no", "boundary"],
  no_routine: ["routine", "schedule"],

  fear_rejection: ["rejection", "no"],
  imposter: ["imposter", "fraud"],
  comparison: ["compare", "other"],
  burnout: ["burnout", "tired", "exhaust"],

  who_to_hire: ["hire", "first"],
  trust_issues: ["trust", "control"],
  accountability: ["accountab", "deliver"]
};
