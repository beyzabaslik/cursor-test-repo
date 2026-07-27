/** Mock dashboard data for the YC demo screen. */

export const valueProposition = {
  title: "Company Brain",
  subtitle: "Company knowledge + workflows + AI agents — working together.",
  description:
    "One place where your docs, tools, and processes connect to autonomous agents that actually execute work.",
};

export const knowledgeMetrics = [
  {
    id: "documents",
    label: "Documents",
    value: "1,247",
    change: "+84 this week",
    icon: "📄",
  },
  {
    id: "tools",
    label: "Connected Tools",
    value: "38",
    change: "Slack, Notion, GitHub +35",
    icon: "🔌",
  },
  {
    id: "nodes",
    label: "Knowledge Nodes",
    value: "892",
    change: "Semantic graph synced",
    icon: "🧠",
  },
];

export const agents = [
  {
    id: "cursor",
    name: "Cursor Agent",
    role: "Engineering execution",
    description: "Ships code, specs, and refactors using full company context.",
    status: "active",
    tasksToday: 14,
    accent: "#3b82f6",
    initials: "CR",
  },
  {
    id: "claude",
    name: "Claude Agent",
    role: "Analysis & communication",
    description: "Drafts decisions, reports, and stakeholder updates from live knowledge.",
    status: "active",
    tasksToday: 9,
    accent: "#d97706",
    initials: "CL",
  },
  {
    id: "knowledge",
    name: "Knowledge Agent",
    role: "Retrieval & synthesis",
    description: "Finds answers across docs, wikis, and past workflows in seconds.",
    status: "active",
    tasksToday: 27,
    accent: "#10b981",
    initials: "KN",
  },
];

export const workflows = [
  {
    id: "wf-1",
    title: "Q3 Product Launch Brief",
    agent: "Cursor Agent",
    agentId: "cursor",
    status: "completed",
    time: "2m ago",
  },
  {
    id: "wf-2",
    title: "Customer Onboarding SOP Update",
    agent: "Knowledge Agent",
    agentId: "knowledge",
    status: "in_progress",
    time: "12m ago",
  },
  {
    id: "wf-3",
    title: "Competitive Analysis Report",
    agent: "Claude Agent",
    agentId: "claude",
    status: "completed",
    time: "1h ago",
  },
  {
    id: "wf-4",
    title: "API Integration Spec",
    agent: "Cursor Agent",
    agentId: "cursor",
    status: "queued",
    time: "5m ago",
  },
];

export const statusLabels = {
  completed: "Completed",
  in_progress: "In Progress",
  queued: "Queued",
};
