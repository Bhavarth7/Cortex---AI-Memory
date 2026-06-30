import { motion } from "framer-motion";
import { ArrowUpRight, Brain } from "lucide-react";

interface ImprovementBannerProps {
  prev: number;
  current: number;
}

export function ImprovementBanner({ prev, current }: ImprovementBannerProps) {
  const delta = current - prev;
  if (delta <= 0.001) return null;
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      className="relative overflow-hidden rounded-2xl border border-good/25 p-5"
      style={{
        background:
          "linear-gradient(120deg, rgba(52,211,153,0.10), rgba(34,211,238,0.06))",
      }}
    >
      <div className="flex items-center gap-4">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-good/15 text-good">
          <Brain className="h-5 w-5" />
        </div>
        <div className="flex-1">
          <div className="text-sm font-semibold text-ink">Learned from prior run</div>
          <div className="text-xs text-ink-soft">
            Regulated-domain memory was retrieved and applied. Controls landed on the
            first pass — no late critique needed.
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center gap-1 text-good">
            <ArrowUpRight className="h-4 w-4" />
            <span className="num text-2xl font-bold">+{Math.round(delta * 100)}</span>
          </div>
          <div className="num text-[11px] text-ink-faint">
            {Math.round(prev * 100)} → {Math.round(current * 100)}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
