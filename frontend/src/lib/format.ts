import type { Decision, Severity } from "../types";

export function agentLabel(name: string): string {
  return name
    .replace(/_agent$/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function dimLabel(name: string): string {
  return name.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function pct(n: number): string {
  return `${Math.round(n * 100)}`;
}

/** Color token for a 0..1 score. */
export function scoreColor(n: number): string {
  if (n < 0.5) return "var(--color-bad)";
  if (n < 0.75) return "var(--color-warn)";
  return "var(--color-good)";
}

export function decisionTone(d: Decision): {
  label: string;
  fg: string;
  bg: string;
} {
  switch (d) {
    case "approve":
      return { label: "Approved", fg: "#34d399", bg: "rgba(52,211,153,0.12)" };
    case "revise":
      return { label: "Revise", fg: "#fbbf24", bg: "rgba(251,191,36,0.12)" };
    case "escalate":
      return { label: "Escalate", fg: "#fb7185", bg: "rgba(251,113,133,0.12)" };
  }
}

export function severityTone(s: Severity): string {
  switch (s) {
    case "critical":
      return "var(--color-bad)";
    case "high":
      return "#fb923c";
    case "medium":
      return "var(--color-warn)";
    default:
      return "var(--color-ink-faint)";
  }
}

export function eventLabel(type: string): string {
  return type.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
