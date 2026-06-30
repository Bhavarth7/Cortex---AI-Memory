import { Panel, PanelHeader } from "./ui/Panel";
import { ScoreBar } from "./ui/ScoreBar";
import { Scale } from "lucide-react";
import { CRITICAL_DIMENSIONS, type ConsensusDecision } from "../types";
import { decisionTone, dimLabel } from "../lib/format";

export function ConsensusPanel({ consensus }: { consensus: ConsensusDecision | null }) {
  if (!consensus) return null;
  const tone = decisionTone(consensus.decision);
  const dims = Object.entries(consensus.per_dimension);

  return (
    <Panel>
      <PanelHeader
        title="Consensus"
        subtitle="Reputation-weighted, per dimension"
        icon={<Scale className="h-4 w-4" />}
        right={
          <span
            className="rounded-full px-3 py-1 text-xs font-semibold"
            style={{ color: tone.fg, background: tone.bg, border: `1px solid ${tone.fg}33` }}
          >
            {tone.label}
          </span>
        }
      />
      <div className="grid grid-cols-2 gap-x-6 gap-y-3 px-5 pb-4 pt-1">
        {dims.map(([dim, score], i) => (
          <ScoreBar
            key={dim}
            label={dimLabel(dim)}
            value={score}
            critical={CRITICAL_DIMENSIONS.includes(dim)}
            delay={i * 0.05}
          />
        ))}
      </div>
      <div className="flex items-center justify-between border-t border-line px-5 py-3 text-xs">
        <span className="text-ink-faint">
          Overall <span className="num font-semibold text-ink-soft">{(consensus.overall_score * 100).toFixed(0)}</span>
          <span className="mx-2 text-line-strong">·</span>
          Conflict <span className="num font-semibold text-ink-soft">{consensus.conflict.toFixed(3)}</span>
        </span>
        {consensus.failed_critical.length > 0 ? (
          <span className="text-bad">
            Failed critical: {consensus.failed_critical.map(dimLabel).join(", ")}
          </span>
        ) : (
          <span className="text-good">All critical dimensions passed</span>
        )}
      </div>
    </Panel>
  );
}
