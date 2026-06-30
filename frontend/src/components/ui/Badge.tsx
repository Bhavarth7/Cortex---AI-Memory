import type { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  fg?: string;
  bg?: string;
  border?: string;
}

export function Badge({
  children,
  fg = "var(--color-ink-soft)",
  bg = "var(--color-base-800)",
  border = "var(--color-line)",
}: BadgeProps) {
  return (
    <span
      className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[11px] font-medium"
      style={{ color: fg, background: bg, border: `1px solid ${border}` }}
    >
      {children}
    </span>
  );
}
