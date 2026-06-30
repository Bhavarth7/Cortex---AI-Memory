import type { ExecutionPackage, ReputationRow } from "../types";
import { MOCK_REPUTATION, RUN_1, RUN_2 } from "../data/mock";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function tryFetch<T>(path: string, init?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(`${BASE}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
      signal: AbortSignal.timeout(4000),
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

/** Run a task. Falls back to mock data when the backend is unreachable. */
export async function runTask(
  task: string,
  isFirstRegulatedRun: boolean,
): Promise<{ pkg: ExecutionPackage; live: boolean }> {
  const live = await tryFetch<ExecutionPackage>("/run", {
    method: "POST",
    body: JSON.stringify({ task }),
  });
  if (live) return { pkg: live, live: true };
  // Offline: pick the run that best illustrates the loop.
  const pkg = isFirstRegulatedRun ? RUN_1 : RUN_2;
  return { pkg: { ...pkg, problem_understanding: task || pkg.problem_understanding }, live: false };
}

export async function fetchReputation(): Promise<{
  rows: ReputationRow[];
  live: boolean;
}> {
  const live = await tryFetch<ReputationRow[]>("/reputation");
  if (live && live.length) return { rows: live, live: true };
  return { rows: MOCK_REPUTATION, live: false };
}
