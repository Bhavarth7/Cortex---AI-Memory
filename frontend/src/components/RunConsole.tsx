import { useState } from "react";
import { Sparkles, CornerDownLeft, Loader2 } from "lucide-react";

interface RunConsoleProps {
  onRun: (task: string) => void;
  loading: boolean;
}

const EXAMPLES = [
  "Build a healthcare RAG assistant for patient records",
  "Build an insurance claims RAG assistant",
  "Design a real-time fraud detection pipeline",
];

export function RunConsole({ onRun, loading }: RunConsoleProps) {
  const [task, setTask] = useState(EXAMPLES[0]);

  return (
    <div className="panel p-5">
      <div className="mb-3 flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-accent" />
        <span className="text-sm font-semibold tracking-tight">Pose a problem</span>
      </div>
      <div className="relative">
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          rows={2}
          placeholder="Describe an ambiguous technical problem…"
          className="w-full resize-none rounded-xl border border-line bg-base-950/60 px-4 py-3 pr-32 text-sm text-ink outline-none transition-colors placeholder:text-ink-faint focus:border-accent/40"
        />
        <button
          onClick={() => onRun(task)}
          disabled={loading || !task.trim()}
          className="absolute bottom-3 right-3 inline-flex items-center gap-2 rounded-lg bg-accent px-3.5 py-2 text-xs font-semibold text-base-950 transition-opacity hover:opacity-90 disabled:opacity-40"
        >
          {loading ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <CornerDownLeft className="h-3.5 w-3.5" />
          )}
          {loading ? "Running team…" : "Run team"}
        </button>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <span className="text-[11px] text-ink-faint">Try:</span>
        {EXAMPLES.map((ex) => (
          <button
            key={ex}
            onClick={() => setTask(ex)}
            className="rounded-full border border-line bg-base-850 px-2.5 py-1 text-[11px] text-ink-soft transition-colors hover:border-line-strong hover:text-ink"
          >
            {ex}
          </button>
        ))}
      </div>
    </div>
  );
}
