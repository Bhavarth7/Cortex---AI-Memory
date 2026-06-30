import type { ReactNode } from "react";

interface PanelProps {
  children: ReactNode;
  className?: string;
}

export function Panel({ children, className = "" }: PanelProps) {
  return <div className={`panel ${className}`}>{children}</div>;
}

interface PanelHeaderProps {
  title: string;
  subtitle?: string;
  icon?: ReactNode;
  right?: ReactNode;
}

export function PanelHeader({ title, subtitle, icon, right }: PanelHeaderProps) {
  return (
    <div className="flex items-start justify-between gap-4 px-5 pt-4 pb-3">
      <div className="flex items-center gap-3">
        {icon && (
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-base-800 text-accent">
            {icon}
          </div>
        )}
        <div>
          <h3 className="text-sm font-semibold tracking-tight text-ink">{title}</h3>
          {subtitle && (
            <p className="text-xs text-ink-faint">{subtitle}</p>
          )}
        </div>
      </div>
      {right}
    </div>
  );
}
