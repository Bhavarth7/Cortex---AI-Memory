import { useEffect, useState } from "react";
import { Sidebar } from "./components/layout/Sidebar";
import { Topbar } from "./components/layout/Topbar";
import { RunConsole } from "./components/RunConsole";
import { PipelineFlow } from "./components/PipelineFlow";
import { DebateGraph } from "./components/DebateGraph";
import { ConsensusPanel } from "./components/ConsensusPanel";
import { ReputationPanel } from "./components/ReputationPanel";
import { TraceTimeline } from "./components/TraceTimeline";
import { ImprovementBanner } from "./components/ImprovementBanner";
import { Panel, PanelHeader } from "./components/ui/Panel";
import { StatCard } from "./components/ui/StatCard";
import { Gauge, GitBranch, ShieldAlert, Network } from "lucide-react";
import { runTask, fetchReputation } from "./api/client";
import { decisionTone } from "./lib/format";
import type { ExecutionPackage, ReputationRow } from "./types";
import { RUN_1, MOCK_REPUTATION } from "./data/mock";

function Section({ id, children }: { id: string; children: React.ReactNode }) {
  return (
    <section id={id} style={{ scrollMarginTop: 76 }}>
      {children}
    </section>
  );
}

export default function App() {
  const [pkg, setPkg] = useState<ExecutionPackage>(RUN_1);
  const [prevScore, setPrevScore] = useState<number | null>(null);
  const [reputation, setReputation] = useState<ReputationRow[]>(MOCK_REPUTATION);
  const [live, setLive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [runIdx, setRunIdx] = useState(0);
  const [active, setActive] = useState("console");

  useEffect(() => {
    fetchReputation().then((r) => {
      setReputation(r.rows);
      setLive(r.live);
    });
  }, []);

  async function handleRun(task: string) {
    setLoading(true);
    const next = runIdx + 1;
    const result = await runTask(task, next % 2 === 1);
    setPrevScore(pkg.evaluator_score);
    setPkg(result.pkg);
    setLive(result.live);
    setRunIdx(next);
    const rep = await fetchReputation();
    setReputation(rep.rows);
    setLoading(false);
  }

  function navigate(id: string) {
    setActive(id);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  const tone = pkg.consensus ? decisionTone(pkg.consensus.decision) : null;
  const provider = live ? "qwen" : "mock";

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar active={active} onNavigate={navigate} live={live} provider={provider} />

      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar taskId={pkg.task_id} tags={pkg.tags} />

        <main className="flex-1 space-y-5 overflow-y-auto px-6 py-6">
          <Section id="console">
            <RunConsole onRun={handleRun} loading={loading} />
          </Section>

          <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
            <StatCard
              label="Decision"
              value={tone?.label ?? "—"}
              accent={tone?.fg}
              icon={<Network className="h-4 w-4" />}
              hint={pkg.consensus ? `overall ${Math.round(pkg.consensus.overall_score * 100)}` : ""}
            />
            <StatCard
              label="Evaluator Score"
              value={Math.round(pkg.evaluator_score * 100)}
              accent="var(--color-good)"
              icon={<Gauge className="h-4 w-4" />}
              delay={0.05}
              hint={
                prevScore != null && pkg.evaluator_score > prevScore
                  ? `up from ${Math.round(prevScore * 100)}`
                  : pkg.first_pass_complete
                    ? "complete on first pass"
                    : "penalized: late catch"
              }
            />
            <StatCard
              label="Conflict"
              value={pkg.consensus ? pkg.consensus.conflict.toFixed(3) : "—"}
              accent="var(--color-accent)"
              icon={<GitBranch className="h-4 w-4" />}
              delay={0.1}
              hint="vote variance"
            />
            <StatCard
              label="Revisions"
              value={pkg.revisions}
              accent={pkg.revisions ? "var(--color-warn)" : "var(--color-ink-soft)"}
              icon={<ShieldAlert className="h-4 w-4" />}
              delay={0.15}
              hint={pkg.critiques.length ? `${pkg.critiques.length} critique(s)` : "no blocking critiques"}
            />
          </div>

          <PipelineFlow revised={pkg.revisions > 0} />

          {prevScore != null && (
            <ImprovementBanner prev={prevScore} current={pkg.evaluator_score} />
          )}

          <Section id="debate">
            <Panel>
              <PanelHeader
                title="Debate Graph"
                subtitle="Proposals, critiques, revision, and consensus"
                icon={<Network className="h-4 w-4" />}
              />
              <DebateGraph pkg={pkg} />
            </Panel>
          </Section>

          <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
            <Section id="consensus">
              <ConsensusPanel consensus={pkg.consensus} />
            </Section>
            <Section id="reputation">
              <ReputationPanel rows={reputation} />
            </Section>
          </div>

          <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
            <Section id="trace">
              <TraceTimeline events={pkg.trace} />
            </Section>
            <Panel>
              <PanelHeader
                title="Risk Register"
                subtitle="Surfaced by the Risk/Security agent"
                icon={<ShieldAlert className="h-4 w-4" />}
              />
              <ul className="space-y-2 px-5 pb-5 pt-1">
                {pkg.risk_register.length ? (
                  pkg.risk_register.map((r, i) => (
                    <li key={i} className="flex items-start gap-2.5 text-sm text-ink-soft">
                      <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-bad" />
                      {r}
                    </li>
                  ))
                ) : (
                  <li className="text-sm text-ink-faint">No risks recorded.</li>
                )}
              </ul>
            </Panel>
          </div>

          <footer className="py-4 text-center text-[11px] text-ink-faint">
            Cortex · memory-augmented, reputation-weighted multi-agent planning
          </footer>
        </main>
      </div>
    </div>
  );
}
