import { motion } from "framer-motion";
import { Panel, PanelHeader } from "./ui/Panel";
import { Activity } from "lucide-react";
import type { TraceEvent } from "../types";
import { eventLabel } from "../lib/format";

const EVENT_COLOR: Record<string, string> = {
  task_created: "#8b5cf6",
  memory_retrieved: "#a78bfa",
  proposal_created: "#38bdf8",
  first_pass_assessed: "#22d3ee",
  critique_raised: "#fb7185",
  revision_applied: "#fb923c",
  vote_phase: "#2dd4bf",
  consensus_reached: "#22d3ee",
  evaluation: "#fbbf24",
  reputation_updated: "#34d399",
  memory_written: "#a78bfa",
};

function summarize(e: TraceEvent): string {
  const p = e.payload as Record<string, unknown>;
  if (e.event_type === "critique_raised") return `${p.from} · ${p.severity}`;
  if (e.event_type === "consensus_reached") return String(p.decision ?? "");
  if (e.event_type === "evaluation") return `score ${p.evaluator_score ?? ""}`;
  if (e.event_type === "memory_retrieved") return `procedural ${p.procedural} · case ${p.case}`;
  if (e.event_type === "memory_written") return `case ${p.case} · procedural ${p.procedural}`;
  if (e.event_type === "first_pass_assessed") return p.complete ? "complete" : "incomplete";
  if (e.event_type === "vote_phase") return `${p.votes} votes`;
  return "";
}

export function TraceTimeline({ events }: { events: TraceEvent[] }) {
  return (
    <Panel>
      <PanelHeader
        title="Trace Replay"
        subtitle={`${events.length} events`}
        icon={<Activity className="h-4 w-4" />}
      />
      <div className="relative px-5 pb-5 pt-1">
        <div className="absolute bottom-5 left-[26px] top-1 w-px bg-line" />
        {events.map((e, i) => {
          const color = EVENT_COLOR[e.event_type] ?? "var(--color-ink-faint)";
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -6 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.04 }}
              className="relative flex items-center gap-3 py-1.5"
            >
              <span
                className="z-10 h-2.5 w-2.5 shrink-0 rounded-full ring-4 ring-base-900"
                style={{ background: color }}
              />
              <span className="text-xs font-medium text-ink">{eventLabel(e.event_type)}</span>
              <span className="num flex-1 truncate text-[11px] text-ink-faint">{summarize(e)}</span>
              <span className="num text-[10px] text-ink-faint">{e.created_at.slice(-8)}</span>
            </motion.div>
          );
        })}
      </div>
    </Panel>
  );
}
