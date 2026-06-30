import { motion } from "framer-motion";
import { ChevronRight } from "lucide-react";

const STAGES = [
  "Retrieve memory",
  "Propose",
  "Critique",
  "Revise",
  "Vote",
  "Consensus",
  "Evaluate",
  "Learn",
];

interface PipelineFlowProps {
  revised: boolean;
}

export function PipelineFlow({ revised }: PipelineFlowProps) {
  return (
    <div className="panel flex items-center gap-1 overflow-x-auto px-5 py-4">
      {STAGES.map((stage, i) => {
        const skipped = stage === "Revise" && !revised;
        return (
          <div key={stage} className="flex items-center gap-1">
            <motion.div
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="flex items-center gap-2 whitespace-nowrap rounded-lg border px-3 py-1.5"
              style={{
                borderColor: skipped ? "var(--color-line)" : "rgba(34,211,238,0.25)",
                background: skipped ? "transparent" : "rgba(34,211,238,0.06)",
                opacity: skipped ? 0.4 : 1,
              }}
            >
              <span
                className="num text-[10px] font-semibold"
                style={{ color: skipped ? "var(--color-ink-faint)" : "var(--color-accent)" }}
              >
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="text-xs font-medium text-ink">{stage}</span>
            </motion.div>
            {i < STAGES.length - 1 && (
              <ChevronRight className="h-3.5 w-3.5 shrink-0 text-ink-faint" />
            )}
          </div>
        );
      })}
    </div>
  );
}
