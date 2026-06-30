import { motion } from "framer-motion";
import { scoreColor, pct } from "../../lib/format";

interface ScoreBarProps {
  label: string;
  value: number;
  critical?: boolean;
  delay?: number;
}

export function ScoreBar({ label, value, critical, delay = 0 }: ScoreBarProps) {
  const color = scoreColor(value);
  const failed = critical && value < 0.5;
  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between">
        <span className="flex items-center gap-1.5 text-xs text-ink-soft">
          {label}
          {critical && (
            <span
              className="rounded px-1 py-px text-[9px] font-semibold uppercase tracking-wide"
              style={{
                color: failed ? "var(--color-bad)" : "var(--color-ink-faint)",
                background: failed ? "rgba(251,113,133,0.12)" : "transparent",
                border: `1px solid ${failed ? "rgba(251,113,133,0.3)" : "var(--color-line)"}`,
              }}
            >
              critical
            </span>
          )}
        </span>
        <span className="num text-xs font-semibold" style={{ color }}>
          {pct(value)}
        </span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-base-800">
        <motion.div
          className="h-full rounded-full"
          style={{ background: `linear-gradient(90deg, ${color}aa, ${color})` }}
          initial={{ width: 0 }}
          animate={{ width: `${value * 100}%` }}
          transition={{ duration: 0.7, delay, ease: "easeOut" }}
        />
      </div>
    </div>
  );
}
