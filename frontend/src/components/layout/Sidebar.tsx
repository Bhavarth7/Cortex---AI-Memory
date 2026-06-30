import { Hexagon, Circle } from "lucide-react";
import { AGENT_META, AGENT_ORDER } from "../../lib/agents";

interface SidebarProps {
  active: string;
  onNavigate: (id: string) => void;
  live: boolean;
  provider: string;
}

const NAV = [
  { id: "console", label: "Run Console" },
  { id: "debate", label: "Debate Graph" },
  { id: "consensus", label: "Consensus" },
  { id: "reputation", label: "Reputation" },
  { id: "trace", label: "Trace" },
];

export function Sidebar({ active, onNavigate, live, provider }: SidebarProps) {
  return (
    <aside className="flex h-full w-64 shrink-0 flex-col border-r border-line bg-base-900/60">
      <div className="flex items-center gap-2.5 px-5 py-5">
        <div className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-accent/25 to-violet/25 ring-1 ring-line-strong">
          <Hexagon className="h-5 w-5 text-accent" strokeWidth={2.2} />
        </div>
        <div>
          <div className="text-[15px] font-bold leading-none tracking-tight">Cortex</div>
          <div className="mt-0.5 text-[10px] uppercase tracking-[0.18em] text-ink-faint">
            Agent Team
          </div>
        </div>
      </div>

      <nav className="px-3 py-2">
        {NAV.map((item) => {
          const on = active === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className="group relative mb-0.5 flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors"
              style={{
                color: on ? "var(--color-ink)" : "var(--color-ink-soft)",
                background: on ? "var(--color-base-800)" : "transparent",
              }}
            >
              <span
                className="h-1.5 w-1.5 rounded-full transition-colors"
                style={{ background: on ? "var(--color-accent)" : "var(--color-ink-faint)" }}
              />
              {item.label}
            </button>
          );
        })}
      </nav>

      <div className="mt-2 px-5 pb-2 pt-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-ink-faint">
        Engineering Team
      </div>
      <div className="flex-1 space-y-0.5 overflow-y-auto px-3">
        {AGENT_ORDER.map((id) => {
          const a = AGENT_META[id];
          const Icon = a.icon;
          return (
            <div
              key={id}
              className="flex items-center gap-3 rounded-lg px-2 py-1.5 hover:bg-base-850"
            >
              <div
                className="flex h-7 w-7 items-center justify-center rounded-lg"
                style={{ background: `${a.color}1a`, color: a.color }}
              >
                <Icon className="h-3.5 w-3.5" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="truncate text-xs font-medium text-ink">{a.label}</div>
                <div className="truncate text-[10px] text-ink-faint">{a.role}</div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="border-t border-line px-5 py-3">
        <div className="flex items-center justify-between text-[11px]">
          <span className="text-ink-faint">Provider</span>
          <span className="num font-medium text-ink-soft">{provider}</span>
        </div>
        <div className="mt-1.5 flex items-center gap-1.5 text-[11px]">
          <Circle
            className="h-2 w-2"
            fill={live ? "var(--color-good)" : "var(--color-warn)"}
            stroke="none"
          />
          <span className="text-ink-soft">{live ? "Backend live" : "Demo data"}</span>
        </div>
      </div>
    </aside>
  );
}
