import { useMemo } from "react";
import {
  ReactFlow,
  Background,
  BackgroundVariant,
  Handle,
  Position,
  type Node,
  type Edge,
  type NodeProps,
} from "@xyflow/react";
import { AGENT_META, AGENT_ORDER } from "../lib/agents";
import type { ExecutionPackage } from "../types";

type CardData = {
  label: string;
  sub: string;
  color: string;
  kind: "task" | "agent" | "consensus" | "eval";
  flagged?: boolean;
};

function CardNode({ data }: NodeProps<Node<CardData>>) {
  const { label, sub, color, kind, flagged } = data;
  const wide = kind === "task" || kind === "consensus" || kind === "eval";
  return (
    <div
      className="rounded-xl border px-3 py-2 shadow-lg"
      style={{
        width: wide ? 190 : 168,
        background: "linear-gradient(180deg, var(--color-base-800), var(--color-base-900))",
        borderColor: flagged ? "rgba(251,113,133,0.5)" : `${color}40`,
        boxShadow: flagged
          ? "0 0 0 1px rgba(251,113,133,0.25), 0 10px 30px -12px rgba(0,0,0,0.8)"
          : "0 10px 30px -16px rgba(0,0,0,0.9)",
      }}
    >
      <Handle type="target" position={Position.Left} style={{ opacity: 0 }} />
      <div className="flex items-center gap-2">
        <span className="h-2 w-2 rounded-full" style={{ background: color }} />
        <span className="text-[12px] font-semibold text-ink">{label}</span>
        {flagged && (
          <span className="ml-auto rounded bg-[rgba(251,113,133,0.15)] px-1.5 py-px text-[9px] font-semibold uppercase text-bad">
            flagged
          </span>
        )}
      </div>
      <div className="mt-1 text-[10px] leading-tight text-ink-faint">{sub}</div>
      <Handle type="source" position={Position.Right} style={{ opacity: 0 }} />
    </div>
  );
}

const nodeTypes = { card: CardNode };

export function DebateGraph({ pkg }: { pkg: ExecutionPackage }) {
  const { nodes, edges } = useMemo(() => {
    const flaggedAgents = new Set(pkg.critiques.map((c) => c.target_agent));
    const nodes: Node<CardData>[] = [];
    const edges: Edge[] = [];

    nodes.push({
      id: "task",
      type: "card",
      position: { x: 0, y: 230 },
      data: { label: "Problem", sub: pkg.tags.join(" · "), color: "#8b5cf6", kind: "task" },
    });

    AGENT_ORDER.filter((a) => a !== "evaluator_agent").forEach((id, i) => {
      const meta = AGENT_META[id];
      nodes.push({
        id,
        type: "card",
        position: { x: 290, y: i * 96 },
        data: {
          label: meta.label,
          sub: meta.role,
          color: meta.color,
          kind: "agent",
          flagged: flaggedAgents.has(id),
        },
      });
      edges.push({
        id: `task-${id}`,
        source: "task",
        target: id,
        animated: false,
        style: { stroke: "var(--color-line-strong)" },
      });
      edges.push({
        id: `${id}-consensus`,
        source: id,
        target: "consensus",
        style: { stroke: "var(--color-line)" },
      });
    });

    // Critique edges (risk -> architecture), highlighted by severity.
    pkg.critiques.forEach((c, i) => {
      edges.push({
        id: `crit-${i}`,
        source: c.from_agent,
        target: c.target_agent,
        animated: true,
        label: c.severity,
        labelStyle: { fill: "#fb7185", fontSize: 10, fontWeight: 600 },
        labelBgStyle: { fill: "rgba(251,113,133,0.12)" },
        style: { stroke: "#fb7185", strokeWidth: 2 },
      });
    });

    nodes.push({
      id: "consensus",
      type: "card",
      position: { x: 600, y: 200 },
      data: {
        label: "Consensus",
        sub: pkg.consensus ? `${pkg.consensus.decision} · conflict ${pkg.consensus.conflict.toFixed(2)}` : "—",
        color: "#22d3ee",
        kind: "consensus",
      },
    });
    nodes.push({
      id: "evaluator_agent",
      type: "card",
      position: { x: 880, y: 200 },
      data: {
        label: "Evaluator",
        sub: `score ${Math.round(pkg.evaluator_score * 100)}`,
        color: "#fbbf24",
        kind: "eval",
      },
    });
    edges.push({
      id: "consensus-eval",
      source: "consensus",
      target: "evaluator_agent",
      animated: true,
      style: { stroke: "rgba(251,191,36,0.5)", strokeWidth: 1.5 },
    });

    return { nodes, edges };
  }, [pkg]);

  return (
    <div className="h-[440px] w-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.18 }}
        proOptions={{ hideAttribution: true }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        zoomOnScroll={false}
        panOnDrag
      >
        <Background variant={BackgroundVariant.Dots} gap={22} size={1} color="#1c2334" />
      </ReactFlow>
    </div>
  );
}
