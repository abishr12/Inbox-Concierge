const COLOR_PALETTE = [
  "#3b82f6", // blue
  "#ef4444", // red
  "#10b981", // green
  "#f59e0b", // amber
  "#8b5cf6", // violet
  "#ec4899", // pink
  "#14b8a6", // teal
  "#f97316", // orange
  "#06b6d4", // cyan
  "#84cc16", // lime
  "#a855f7", // purple
  "#f43f5e", // rose
  "#0ea5e9", // sky
  "#22c55e", // green-500
  "#eab308", // yellow
  "#6366f1", // indigo
  "#d946ef", // fuchsia
  "#64748b", // slate
  "#78716c", // stone
  "#6b7280", // gray
];

export const generateRandomColor = (): string => {
  const randomIndex = Math.floor(Math.random() * COLOR_PALETTE.length);
  return COLOR_PALETTE[randomIndex];
};
