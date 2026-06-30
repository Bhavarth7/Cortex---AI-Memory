import { motion } from "framer-motion";
import { Panel, PanelHeader } from "./ui/Panel";
import { TrendingUp } from "lucide-react";
import type { ReputationRow } from "../types";
import { AGENT_META } from "../lib/agents";
import { agentLabel, dimLabel, scoreColor } from "../lib/format";

export function ReputationPanel({ rows }: { rows: ReputationRow[] }) {
  return (
    <Panel>
      <PanelHeader
        title="Reputation"
        subtitle="Confidence-weighted, per skill"
        icon={<TrendingUp className="h-4 w-4" />}
      />
      <div className="space-y-1 px-3 pb-4">
        {rows.map((r, i) => {
          const meta = AGENT_META[r.agent_name];
          const color = meta?.color ?? "var(--color-accent)";
          return (
            <motion.div
              key={`${r.agent_name}-${r.skill}`}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-center gap-3 rounded-lg px-2 py-2 hover:bg-base-850"
            >
              <span className="h-2 w-2 shrink-0 rounded-full" style={{ background: color }} />
              <div className="w-28 shrink-0">
                <div className="text-xs font-medium text-ink">{agentLabel(r.agent_name)}</div>
                <div className="text-[10px] text-ink-faint">{dimLabel(r.skill)}</div>
              </div>
              <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-base-800">
                <motion.div
                  className="h-full rounded-full"
                  style={{ background: scoreColor(r.reputation_score) }}
                  initial={{ width: 0 }}
                  animate={{ width: `${r.reputation_score * 100}%` }}
                  transition={{ duration: 0.7, delay: i * 0.05 }}
                />
              </div>
              <span className="num w-9 text-right text-xs font-semibold text-ink-soft">
                {r.reputation_score.toFixed(2)}
              </span>
              <span className="num w-12 text-right text-[10px] text-ink-faint">
                n={r.observations}
              </span>
            </motion.div>
          );
        })}
      </div>
    </Panel>
  );
}
