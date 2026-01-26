// Problem Wizard Hierarchy - Choose Your Own Adventure Style
// 5-step funnel: Core Struggle → Focus Area → Root Cause → Specific Situation → Custom Context

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

// Step 1: Core Struggle - The big picture question
export const STEP_1_CORE_STRUGGLES: WizardStep = {
  id: "core_struggle",
  title: "What's holding you back?",
  subtitle: "Let's start with the big picture",
  options: [
    {
      id: "more_business",
      label: "I need to FIND more opportunities",
      description: "Meeting new people, generating leads, filling my pipeline",
      icon: "🔍"
    },
    {
      id: "close_more",
      label: "I need to WIN more of my opportunities",
      description: "Converting the leads I have, closing deals, getting to yes",
      icon: "🏆"
    },
    {
      id: "work_smarter",
      label: "I need to WORK SMARTER",
      description: "Better systems, time management, less chaos",
      icon: "⚡"
    },
    {
      id: "grow_personally",
      label: "I need to LEVEL UP as a professional",
      description: "Mindset, confidence, brand, career direction",
      icon: "🚀"
    }
  ]
};

// Step 2: Focus Areas - Drilling down into each core struggle
export const STEP_2_FOCUS_AREAS: { [key: string]: WizardStep } = {
  more_business: {
    id: "focus_area",
    title: "Where are opportunities slipping away?",
    subtitle: "Let's narrow down where to focus",
    options: [
      {
        id: "finding_prospects",
        label: "Finding New Prospects",
        description: "I need fresh leads and new people to talk to",
        icon: "🔍"
      },
      {
        id: "referrals",
        label: "Getting More Referrals",
        description: "My past clients aren't sending me business",
        icon: "🤝"
      },
      {
        id: "social_content",
        label: "Social Media & Content",
        description: "I want to attract clients through my content",
        icon: "📱"
      },
      {
        id: "open_houses_events",
        label: "Open Houses & Events",
        description: "I need better results from open houses",
        icon: "🏠"
      },
      {
        id: "sphere_networking",
        label: "Sphere & Networking",
        description: "I need to better leverage my network",
        icon: "🌐"
      }
    ]
  },
  close_more: {
    id: "focus_area",
    title: "Where are you losing the win?",
    subtitle: "Let's find the bottleneck",
    options: [
      {
        id: "listing_appointments",
        label: "Listing Appointments",
        description: "I'm not winning enough listings",
        icon: "📋"
      },
      {
        id: "buyer_conversion",
        label: "Converting Buyers",
        description: "Buyers won't commit or keep looking forever",
        icon: "🏷️"
      },
      {
        id: "negotiation",
        label: "Negotiation & Offers",
        description: "I lose deals during negotiations",
        icon: "⚖️"
      },
      {
        id: "objections",
        label: "Handling Objections",
        description: "I don't know what to say when they push back",
        icon: "🛡️"
      },
      {
        id: "follow_up",
        label: "Follow-Up & Nurture",
        description: "Leads go cold because I don't follow up well",
        icon: "📞"
      }
    ]
  },
  work_smarter: {
    id: "focus_area",
    title: "What's causing the chaos?",
    subtitle: "Let's identify the pain point",
    options: [
      {
        id: "time_management",
        label: "Time Management",
        description: "I'm always busy but never productive",
        icon: "⏰"
      },
      {
        id: "systems_automation",
        label: "Systems & Automation",
        description: "Everything is manual and messy",
        icon: "⚙️"
      },
      {
        id: "delegation_team",
        label: "Delegation & Team",
        description: "I'm doing everything myself",
        icon: "👥"
      },
      {
        id: "technology",
        label: "Technology & Tools",
        description: "I'm overwhelmed by tech or not using it well",
        icon: "💻"
      },
      {
        id: "work_life_balance",
        label: "Work-Life Balance",
        description: "Real estate is consuming my entire life",
        icon: "⚖️"
      }
    ]
  },
  grow_personally: {
    id: "focus_area",
    title: "What's the real block?",
    subtitle: "Let's get to the heart of it",
    options: [
      {
        id: "confidence_mindset",
        label: "Confidence & Mindset",
        description: "Fear, self-doubt, imposter syndrome",
        icon: "🧠"
      },
      {
        id: "personal_brand",
        label: "Building My Brand",
        description: "I need to stand out and get noticed",
        icon: "✨"
      },
      {
        id: "motivation_burnout",
        label: "Motivation & Burnout",
        description: "I've lost my drive or I'm exhausted",
        icon: "🔥"
      },
      {
        id: "career_direction",
        label: "Career Direction",
        description: "I'm not sure what path to take",
        icon: "🧭"
      },
      {
        id: "market_knowledge",
        label: "Market & Industry Knowledge",
        description: "I need to understand the market better",
        icon: "📊"
      }
    ]
  }
};

// Step 3: Root Causes - Getting to the underlying issue
export const STEP_3_ROOT_CAUSES: { [key: string]: WizardStep } = {
  // MORE BUSINESS → Finding Prospects
  finding_prospects: {
    id: "root_cause",
    title: "What's the real challenge?",
    subtitle: "Pick the one that resonates most",
    options: [
      {
        id: "sphere_tapped",
        label: "My sphere is tapped out",
        description: "I've already talked to everyone I know",
        icon: "😓"
      },
      {
        id: "dont_know_where",
        label: "I don't know where to start",
        description: "There are so many options, I'm paralyzed",
        icon: "🤷"
      },
      {
        id: "hate_cold_outreach",
        label: "I hate cold calling/outreach",
        description: "It feels salesy and uncomfortable",
        icon: "😰"
      },
      {
        id: "nothing_works",
        label: "Nothing seems to work",
        description: "I've tried things but no results",
        icon: "😤"
      },
      {
        id: "new_market",
        label: "I'm new to this market",
        description: "I don't have connections here yet",
        icon: "🆕"
      }
    ]
  },
  // MORE BUSINESS → Referrals
  referrals: {
    id: "root_cause",
    title: "Why aren't referrals coming?",
    subtitle: "What's the disconnect?",
    options: [
      {
        id: "dont_ask",
        label: "I don't ask for them",
        description: "It feels awkward to ask",
        icon: "🤐"
      },
      {
        id: "no_system",
        label: "I have no referral system",
        description: "I don't stay in touch with past clients",
        icon: "📭"
      },
      {
        id: "not_memorable",
        label: "I'm not memorable enough",
        description: "They forget about me",
        icon: "👻"
      },
      {
        id: "bad_experience",
        label: "Maybe the experience wasn't great",
        description: "I'm not sure they'd recommend me",
        icon: "😟"
      }
    ]
  },
  // MORE BUSINESS → Social/Content
  social_content: {
    id: "root_cause",
    title: "What's blocking your content?",
    subtitle: "Where's the struggle?",
    options: [
      {
        id: "hate_camera",
        label: "I hate being on camera",
        description: "I'm uncomfortable with video",
        icon: "📷"
      },
      {
        id: "no_ideas",
        label: "I don't know what to post",
        description: "I run out of content ideas",
        icon: "💭"
      },
      {
        id: "no_engagement",
        label: "Nobody engages with my content",
        description: "I post but nothing happens",
        icon: "👻"
      },
      {
        id: "no_time_content",
        label: "I don't have time for content",
        description: "It takes too long to create",
        icon: "⏰"
      },
      {
        id: "feels_cheesy",
        label: "It feels cheesy or salesy",
        description: "I don't want to be 'that' agent",
        icon: "🧀"
      }
    ]
  },
  // MORE BUSINESS → Open Houses
  open_houses_events: {
    id: "root_cause",
    title: "What's not working?",
    subtitle: "Where's the breakdown?",
    options: [
      {
        id: "no_traffic",
        label: "Nobody shows up",
        description: "Low attendance at my open houses",
        icon: "🦗"
      },
      {
        id: "no_conversion_oh",
        label: "I get visitors but no clients",
        description: "They come, they leave, nothing happens",
        icon: "🚶"
      },
      {
        id: "no_listings_oh",
        label: "I can't get listings to hold open",
        description: "Other agents won't let me do open houses",
        icon: "🔒"
      },
      {
        id: "no_follow_up_oh",
        label: "I don't follow up well after",
        description: "I collect info but never call",
        icon: "📝"
      }
    ]
  },
  // MORE BUSINESS → Sphere/Networking
  sphere_networking: {
    id: "root_cause",
    title: "What's the networking problem?",
    subtitle: "Where does it break down?",
    options: [
      {
        id: "small_sphere",
        label: "My sphere is too small",
        description: "I just don't know many people",
        icon: "📉"
      },
      {
        id: "not_reaching_out",
        label: "I don't reach out enough",
        description: "I let relationships go cold",
        icon: "🧊"
      },
      {
        id: "sphere_no_buy",
        label: "My sphere doesn't buy/sell",
        description: "Wrong demographic or renters",
        icon: "🏢"
      },
      {
        id: "networking_uncomfortable",
        label: "Networking feels uncomfortable",
        description: "I'm introverted or it feels fake",
        icon: "😣"
      }
    ]
  },
  // CLOSE MORE → Listing Appointments
  listing_appointments: {
    id: "root_cause",
    title: "Where do you lose listings?",
    subtitle: "When does it fall apart?",
    options: [
      {
        id: "never_get_appointment",
        label: "I can't get the appointment",
        description: "Sellers won't meet with me",
        icon: "🚪"
      },
      {
        id: "lose_to_competition",
        label: "I lose to other agents",
        description: "They choose someone else",
        icon: "🥈"
      },
      {
        id: "pricing_issues",
        label: "We disagree on price",
        description: "They want too much or I can't justify mine",
        icon: "💰"
      },
      {
        id: "commission_objection",
        label: "They object to commission",
        description: "They want to negotiate my fee",
        icon: "📉"
      }
    ]
  },
  // CLOSE MORE → Buyer Conversion
  buyer_conversion: {
    id: "root_cause",
    title: "Where do buyers stall?",
    subtitle: "What's the pattern?",
    options: [
      {
        id: "wont_commit",
        label: "They won't commit",
        description: "Always looking, never deciding",
        icon: "🔄"
      },
      {
        id: "ghost_buyers",
        label: "They ghost me",
        description: "Stop responding out of nowhere",
        icon: "👻"
      },
      {
        id: "lose_to_other_agent",
        label: "They go with another agent",
        description: "I can't keep them loyal",
        icon: "💔"
      },
      {
        id: "scared_of_market",
        label: "They're scared of the market",
        description: "Worried about rates, prices, timing",
        icon: "😨"
      }
    ]
  },
  // CLOSE MORE → Negotiation
  negotiation: {
    id: "root_cause",
    title: "Where do negotiations fail?",
    subtitle: "What's the sticking point?",
    options: [
      {
        id: "multiple_offers",
        label: "I lose in multiple offer situations",
        description: "My clients keep getting outbid",
        icon: "📊"
      },
      {
        id: "inspection_falls_apart",
        label: "Deals fall apart at inspection",
        description: "Can't navigate repair negotiations",
        icon: "🔍"
      },
      {
        id: "not_assertive",
        label: "I'm not assertive enough",
        description: "I give in too easily",
        icon: "🤷"
      },
      {
        id: "difficult_other_agent",
        label: "Difficult agents/situations",
        description: "Other side makes it hard",
        icon: "😤"
      }
    ]
  },
  // CLOSE MORE → Objections
  objections: {
    id: "root_cause",
    title: "What objection trips you up?",
    subtitle: "Which one do you dread?",
    options: [
      {
        id: "commission_objection_detail",
        label: "\"Your commission is too high\"",
        description: "Justifying your value",
        icon: "💵"
      },
      {
        id: "thinking_about_it",
        label: "\"We need to think about it\"",
        description: "The stall tactic",
        icon: "🤔"
      },
      {
        id: "interviewing_others",
        label: "\"We're interviewing other agents\"",
        description: "Competition concerns",
        icon: "👥"
      },
      {
        id: "friend_in_business",
        label: "\"We have a friend in the business\"",
        description: "The loyalty objection",
        icon: "🤝"
      }
    ]
  },
  // CLOSE MORE → Follow Up
  follow_up: {
    id: "root_cause",
    title: "Why is follow-up failing?",
    subtitle: "What's the breakdown?",
    options: [
      {
        id: "no_follow_up_system",
        label: "I have no system",
        description: "Leads fall through the cracks",
        icon: "🕳️"
      },
      {
        id: "dont_know_what_to_say",
        label: "I don't know what to say",
        description: "Follow-up feels awkward",
        icon: "🤐"
      },
      {
        id: "too_many_leads",
        label: "I have too many leads to manage",
        description: "Overwhelmed by volume",
        icon: "🌊"
      },
      {
        id: "procrastinate_follow_up",
        label: "I procrastinate on calls",
        description: "I avoid picking up the phone",
        icon: "😬"
      }
    ]
  },
  // WORK SMARTER → Time Management
  time_management: {
    id: "root_cause",
    title: "Where does time go?",
    subtitle: "What's eating your hours?",
    options: [
      {
        id: "always_reactive",
        label: "I'm always reactive",
        description: "Constantly putting out fires",
        icon: "🔥"
      },
      {
        id: "cant_say_no",
        label: "I can't say no",
        description: "I take on too much",
        icon: "🙋"
      },
      {
        id: "no_routine",
        label: "I have no routine",
        description: "Every day is chaos",
        icon: "🎲"
      },
      {
        id: "shiny_object",
        label: "Shiny object syndrome",
        description: "I jump between tasks",
        icon: "✨"
      }
    ]
  },
  // WORK SMARTER → Systems
  systems_automation: {
    id: "root_cause",
    title: "What needs systematizing?",
    subtitle: "Where's the biggest mess?",
    options: [
      {
        id: "crm_mess",
        label: "My CRM is a mess (or nonexistent)",
        description: "No organized database",
        icon: "📊"
      },
      {
        id: "transaction_chaos",
        label: "Transaction management is chaotic",
        description: "Balls getting dropped",
        icon: "🎪"
      },
      {
        id: "marketing_inconsistent",
        label: "Marketing is inconsistent",
        description: "No regular system",
        icon: "📅"
      },
      {
        id: "everything_manual",
        label: "Everything is manual",
        description: "No automation at all",
        icon: "✍️"
      }
    ]
  },
  // WORK SMARTER → Delegation
  delegation_team: {
    id: "root_cause",
    title: "What's the delegation block?",
    subtitle: "Why aren't you leveraging help?",
    options: [
      {
        id: "cant_afford_help",
        label: "I can't afford help yet",
        description: "Budget constraints",
        icon: "💸"
      },
      {
        id: "control_freak",
        label: "I'm a control freak",
        description: "Hard to let go",
        icon: "🎮"
      },
      {
        id: "dont_know_what_delegate",
        label: "I don't know what to delegate",
        description: "Not sure what to hand off",
        icon: "❓"
      },
      {
        id: "bad_experiences_team",
        label: "Bad experiences with help",
        description: "It didn't work out before",
        icon: "😞"
      }
    ]
  },
  // WORK SMARTER → Technology
  technology: {
    id: "root_cause",
    title: "What's the tech struggle?",
    subtitle: "Where's the friction?",
    options: [
      {
        id: "overwhelmed_by_tech",
        label: "I'm overwhelmed by options",
        description: "Too many tools, don't know what to use",
        icon: "😵"
      },
      {
        id: "not_using_tech",
        label: "I have tools but don't use them",
        description: "Paying for stuff I ignore",
        icon: "🧊"
      },
      {
        id: "tech_not_working",
        label: "My tech isn't working together",
        description: "Nothing integrates",
        icon: "🔌"
      },
      {
        id: "ai_confused",
        label: "I'm confused about AI",
        description: "Don't know how to leverage it",
        icon: "🤖"
      }
    ]
  },
  // WORK SMARTER → Work-Life Balance
  work_life_balance: {
    id: "root_cause",
    title: "What's out of balance?",
    subtitle: "Where's the struggle?",
    options: [
      {
        id: "always_available",
        label: "I'm always available",
        description: "Can't set boundaries with clients",
        icon: "📱"
      },
      {
        id: "cant_unplug",
        label: "I can't mentally unplug",
        description: "Always thinking about work",
        icon: "🧠"
      },
      {
        id: "family_suffering",
        label: "My relationships are suffering",
        description: "Family/friends feel neglected",
        icon: "👨‍👩‍👧"
      },
      {
        id: "health_suffering",
        label: "My health is suffering",
        description: "No time for self-care",
        icon: "💪"
      }
    ]
  },
  // GROW PERSONALLY → Confidence/Mindset
  confidence_mindset: {
    id: "root_cause",
    title: "What's the mental block?",
    subtitle: "What's really going on?",
    options: [
      {
        id: "imposter_syndrome",
        label: "Imposter syndrome",
        description: "I don't feel qualified",
        icon: "🎭"
      },
      {
        id: "fear_rejection",
        label: "Fear of rejection",
        description: "I hate hearing 'no'",
        icon: "😰"
      },
      {
        id: "comparison_trap",
        label: "Comparing to others",
        description: "Everyone seems more successful",
        icon: "📊"
      },
      {
        id: "fear_success",
        label: "Fear of success",
        description: "What if I actually make it?",
        icon: "😨"
      },
      {
        id: "negative_self_talk",
        label: "Negative self-talk",
        description: "I'm my own worst critic",
        icon: "💬"
      }
    ]
  },
  // GROW PERSONALLY → Personal Brand
  personal_brand: {
    id: "root_cause",
    title: "What's holding back your brand?",
    subtitle: "Where's the gap?",
    options: [
      {
        id: "dont_stand_out",
        label: "I don't stand out",
        description: "I look like every other agent",
        icon: "😐"
      },
      {
        id: "no_niche",
        label: "I don't have a niche",
        description: "I try to be everything to everyone",
        icon: "🎯"
      },
      {
        id: "inconsistent_brand",
        label: "My brand is inconsistent",
        description: "No cohesive message",
        icon: "🧩"
      },
      {
        id: "afraid_to_be_visible",
        label: "I'm afraid to be visible",
        description: "Don't want to put myself out there",
        icon: "🙈"
      }
    ]
  },
  // GROW PERSONALLY → Motivation/Burnout
  motivation_burnout: {
    id: "root_cause",
    title: "What's draining you?",
    subtitle: "Where's the energy leak?",
    options: [
      {
        id: "lost_why",
        label: "I've lost my 'why'",
        description: "Don't remember why I started",
        icon: "❓"
      },
      {
        id: "feast_famine",
        label: "The feast/famine cycle is exhausting",
        description: "Emotional rollercoaster",
        icon: "🎢"
      },
      {
        id: "considering_quitting",
        label: "I'm considering quitting",
        description: "Is this even worth it?",
        icon: "🚪"
      },
      {
        id: "completely_burned_out",
        label: "I'm completely burned out",
        description: "Running on empty",
        icon: "🔋"
      }
    ]
  },
  // GROW PERSONALLY → Career Direction
  career_direction: {
    id: "root_cause",
    title: "What's the career question?",
    subtitle: "What decision are you facing?",
    options: [
      {
        id: "team_or_solo",
        label: "Should I join a team or stay solo?",
        description: "The team decision",
        icon: "👥"
      },
      {
        id: "build_team",
        label: "Should I build my own team?",
        description: "Ready to lead?",
        icon: "🏗️"
      },
      {
        id: "niche_specialize",
        label: "Should I specialize/niche down?",
        description: "Finding my focus",
        icon: "🎯"
      },
      {
        id: "change_brokerages",
        label: "Should I change brokerages?",
        description: "Is the grass greener?",
        icon: "🏠"
      }
    ]
  },
  // GROW PERSONALLY → Market Knowledge
  market_knowledge: {
    id: "root_cause",
    title: "What market knowledge do you need?",
    subtitle: "Where's the gap?",
    options: [
      {
        id: "market_shifts",
        label: "Understanding market shifts",
        description: "What's happening and why",
        icon: "📈"
      },
      {
        id: "talking_rates",
        label: "Talking to clients about rates",
        description: "The interest rate conversation",
        icon: "💬"
      },
      {
        id: "industry_changes",
        label: "Navigating industry changes",
        description: "NAR settlement, commissions, etc.",
        icon: "⚖️"
      },
      {
        id: "competing_discount",
        label: "Competing with discount brokers",
        description: "Proving your value",
        icon: "🏷️"
      }
    ]
  }
};

// Mapping from Step 3 root causes to actual problem categories for Step 4
export const ROOT_CAUSE_TO_CATEGORIES: { [key: string]: string[] } = {
  // MORE BUSINESS → Finding Prospects
  sphere_tapped: ["lead_generation"],
  dont_know_where: ["lead_generation"],
  hate_cold_outreach: ["lead_generation", "mindset_motivation"],
  nothing_works: ["lead_generation"],
  new_market: ["lead_generation"],

  // MORE BUSINESS → Referrals
  dont_ask: ["lead_generation", "mindset_motivation"],
  no_system: ["lead_generation", "systems_operations"],
  not_memorable: ["lead_generation", "personal_brand"],
  bad_experience: ["client_management"],

  // MORE BUSINESS → Social/Content
  hate_camera: ["personal_brand", "mindset_motivation"],
  no_ideas: ["personal_brand"],
  no_engagement: ["personal_brand"],
  no_time_content: ["time_productivity", "personal_brand"],
  feels_cheesy: ["personal_brand", "mindset_motivation"],

  // MORE BUSINESS → Open Houses
  no_traffic: ["lead_generation"],
  no_conversion_oh: ["conversion_sales", "lead_generation"],
  no_listings_oh: ["lead_generation"],
  no_follow_up_oh: ["conversion_sales", "systems_operations"],

  // MORE BUSINESS → Sphere/Networking
  small_sphere: ["lead_generation"],
  not_reaching_out: ["lead_generation", "systems_operations"],
  sphere_no_buy: ["lead_generation"],
  networking_uncomfortable: ["mindset_motivation", "lead_generation"],

  // CLOSE MORE → Listing Appointments
  never_get_appointment: ["lead_generation", "conversion_sales"],
  lose_to_competition: ["conversion_sales", "personal_brand"],
  pricing_issues: ["conversion_sales"],
  commission_objection: ["conversion_sales", "money_business"],

  // CLOSE MORE → Buyer Conversion
  wont_commit: ["conversion_sales"],
  ghost_buyers: ["conversion_sales", "client_management"],
  lose_to_other_agent: ["conversion_sales", "client_management"],
  scared_of_market: ["conversion_sales", "market_industry"],

  // CLOSE MORE → Negotiation
  multiple_offers: ["conversion_sales"],
  inspection_falls_apart: ["conversion_sales"],
  not_assertive: ["conversion_sales", "mindset_motivation"],
  difficult_other_agent: ["conversion_sales"],

  // CLOSE MORE → Objections
  commission_objection_detail: ["conversion_sales", "money_business"],
  thinking_about_it: ["conversion_sales"],
  interviewing_others: ["conversion_sales"],
  friend_in_business: ["conversion_sales"],

  // CLOSE MORE → Follow Up
  no_follow_up_system: ["systems_operations", "conversion_sales"],
  dont_know_what_to_say: ["conversion_sales"],
  too_many_leads: ["systems_operations", "time_productivity"],
  procrastinate_follow_up: ["mindset_motivation", "conversion_sales"],

  // WORK SMARTER → Time Management
  always_reactive: ["time_productivity"],
  cant_say_no: ["time_productivity", "mindset_motivation"],
  no_routine: ["time_productivity"],
  shiny_object: ["time_productivity", "mindset_motivation"],

  // WORK SMARTER → Systems
  crm_mess: ["systems_operations"],
  transaction_chaos: ["systems_operations"],
  marketing_inconsistent: ["systems_operations", "personal_brand"],
  everything_manual: ["systems_operations"],

  // WORK SMARTER → Delegation
  cant_afford_help: ["money_business", "systems_operations"],
  control_freak: ["mindset_motivation", "systems_operations"],
  dont_know_what_delegate: ["systems_operations"],
  bad_experiences_team: ["systems_operations"],

  // WORK SMARTER → Technology
  overwhelmed_by_tech: ["systems_operations"],
  not_using_tech: ["systems_operations"],
  tech_not_working: ["systems_operations"],
  ai_confused: ["systems_operations", "market_industry"],

  // WORK SMARTER → Work-Life Balance
  always_available: ["time_productivity", "client_management"],
  cant_unplug: ["mindset_motivation", "time_productivity"],
  family_suffering: ["time_productivity"],
  health_suffering: ["time_productivity", "mindset_motivation"],

  // GROW PERSONALLY → Confidence/Mindset
  imposter_syndrome: ["mindset_motivation"],
  fear_rejection: ["mindset_motivation"],
  comparison_trap: ["mindset_motivation"],
  fear_success: ["mindset_motivation"],
  negative_self_talk: ["mindset_motivation"],

  // GROW PERSONALLY → Personal Brand
  dont_stand_out: ["personal_brand"],
  no_niche: ["personal_brand"],
  inconsistent_brand: ["personal_brand"],
  afraid_to_be_visible: ["personal_brand", "mindset_motivation"],

  // GROW PERSONALLY → Motivation/Burnout
  lost_why: ["mindset_motivation"],
  feast_famine: ["mindset_motivation", "money_business"],
  considering_quitting: ["mindset_motivation"],
  completely_burned_out: ["mindset_motivation"],

  // GROW PERSONALLY → Career Direction
  team_or_solo: ["money_business", "systems_operations"],
  build_team: ["systems_operations"],
  niche_specialize: ["personal_brand"],
  change_brokerages: ["money_business", "market_industry"],

  // GROW PERSONALLY → Market Knowledge
  market_shifts: ["market_industry"],
  talking_rates: ["market_industry", "conversion_sales"],
  industry_changes: ["market_industry"],
  competing_discount: ["market_industry", "conversion_sales"]
};

// Keywords to filter problems in Step 4 based on root cause selection
export const ROOT_CAUSE_KEYWORDS: { [key: string]: string[] } = {
  sphere_tapped: ["sphere", "database", "network", "referral", "past client"],
  dont_know_where: ["start", "begin", "new agent", "where to"],
  hate_cold_outreach: ["cold", "call", "prospect", "outreach", "phone"],
  nothing_works: ["lead", "generation", "strategy", "convert"],
  new_market: ["new market", "relocat", "unfamiliar", "build"],

  dont_ask: ["ask", "referral", "request"],
  no_system: ["system", "follow", "touch", "stay in"],
  not_memorable: ["memorable", "stand out", "remember", "top of mind"],
  bad_experience: ["client", "experience", "service", "relationship"],

  hate_camera: ["camera", "video", "film", "record", "on-camera"],
  no_ideas: ["content", "idea", "post", "what to"],
  no_engagement: ["engage", "like", "comment", "follow", "audience"],
  no_time_content: ["time", "content", "create", "schedule"],
  feels_cheesy: ["authentic", "cheesy", "salesy", "genuine"],

  no_traffic: ["open house", "traffic", "attend", "visitor"],
  no_conversion_oh: ["open house", "convert", "client", "follow"],
  no_listings_oh: ["listing", "open house", "hold"],
  no_follow_up_oh: ["follow up", "open house", "after"],

  small_sphere: ["sphere", "network", "small", "grow"],
  not_reaching_out: ["reach", "touch", "contact", "stay"],
  sphere_no_buy: ["sphere", "demographic", "rent", "buy"],
  networking_uncomfortable: ["network", "introvert", "uncomfortable", "social"],

  never_get_appointment: ["appointment", "listing", "meet"],
  lose_to_competition: ["compet", "lose", "other agent", "win"],
  pricing_issues: ["price", "pricing", "valuation", "overpriced"],
  commission_objection: ["commission", "fee", "rate", "value"],

  wont_commit: ["commit", "decide", "buyer", "ready"],
  ghost_buyers: ["ghost", "respond", "disappear", "contact"],
  lose_to_other_agent: ["loyalty", "other agent", "leave"],
  scared_of_market: ["market", "rate", "afraid", "wait"],

  multiple_offers: ["multiple offer", "bidding", "compete", "outbid"],
  inspection_falls_apart: ["inspection", "repair", "negotiate"],
  not_assertive: ["assertive", "negotiate", "confident"],
  difficult_other_agent: ["difficult", "agent", "other side"],

  commission_objection_detail: ["commission", "fee", "value", "worth"],
  thinking_about_it: ["think", "decide", "stall", "wait"],
  interviewing_others: ["interview", "other agent", "compet"],
  friend_in_business: ["friend", "family", "loyal", "know"],

  no_follow_up_system: ["follow up", "system", "crm", "track"],
  dont_know_what_to_say: ["say", "script", "conversation", "talk"],
  too_many_leads: ["lead", "volume", "overwhelm", "manage"],
  procrastinate_follow_up: ["procrastin", "avoid", "call", "phone"],

  always_reactive: ["reactive", "proactive", "fire", "urgent"],
  cant_say_no: ["say no", "boundary", "commit", "too much"],
  no_routine: ["routine", "schedule", "morning", "daily"],
  shiny_object: ["focus", "distract", "shiny", "jump"],

  crm_mess: ["crm", "database", "contact", "organize"],
  transaction_chaos: ["transaction", "coordinate", "process", "manage"],
  marketing_inconsistent: ["marketing", "consistent", "regular", "schedule"],
  everything_manual: ["manual", "automat", "tech", "efficiency"],

  cant_afford_help: ["afford", "budget", "cost", "hire"],
  control_freak: ["control", "delegate", "trust", "let go"],
  dont_know_what_delegate: ["delegate", "task", "hire", "help"],
  bad_experiences_team: ["team", "hire", "experience", "manage"],

  overwhelmed_by_tech: ["tech", "tool", "software", "overwhelm"],
  not_using_tech: ["tech", "tool", "use", "implement"],
  tech_not_working: ["integrate", "connect", "tech", "system"],
  ai_confused: ["ai", "artificial", "chatgpt", "technology"],

  always_available: ["available", "boundary", "client", "24/7"],
  cant_unplug: ["unplug", "mental", "stress", "anxiety"],
  family_suffering: ["family", "relationship", "balance", "personal"],
  health_suffering: ["health", "exercise", "sleep", "self-care"],

  imposter_syndrome: ["imposter", "qualify", "enough", "doubt"],
  fear_rejection: ["rejection", "no", "fear", "afraid"],
  comparison_trap: ["compar", "other", "success", "social media"],
  fear_success: ["success", "fear", "achieve", "deserve"],
  negative_self_talk: ["self-talk", "negative", "critic", "voice"],

  dont_stand_out: ["stand out", "different", "unique", "brand"],
  no_niche: ["niche", "specialize", "focus", "target"],
  inconsistent_brand: ["brand", "consistent", "message", "identity"],
  afraid_to_be_visible: ["visible", "public", "social", "put yourself"],

  lost_why: ["why", "purpose", "meaning", "motivation"],
  feast_famine: ["feast", "famine", "inconsistent", "cycle"],
  considering_quitting: ["quit", "leave", "worth", "continue"],
  completely_burned_out: ["burnout", "exhaust", "tired", "energy"],

  team_or_solo: ["team", "solo", "join", "independent"],
  build_team: ["build team", "hire", "grow", "scale"],
  niche_specialize: ["niche", "specialize", "focus", "expert"],
  change_brokerages: ["brokerage", "change", "switch", "move"],

  market_shifts: ["market", "shift", "change", "trend"],
  talking_rates: ["rate", "interest", "mortgage", "conversation"],
  industry_changes: ["industry", "nar", "settlement", "commission"],
  competing_discount: ["discount", "value", "compete", "fee"]
};
