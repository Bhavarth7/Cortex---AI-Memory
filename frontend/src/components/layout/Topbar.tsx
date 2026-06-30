import { Badge } from "../ui/Badge";

interface TopbarProps {
  taskId: number;
  tags: string[];
}

export function Topbar({ taskId, tags }: TopbarProps) {
  return (
    <header className="glass sticky top-0 z-20 flex h-14 items-center justify-between border-b border-line px-6">
      <div className="flex items-center gap-3">
        <h1 className="text-sm font-semibold tracking-tight">
          Multi-Agent Execution Package
        </h1>
        <span className="num text-xs text-ink-faint">#{taskId}</span>
      </div>
      <div className="flex items-center gap-2">
        {tags.map((t) => (
          <Badge key={t} fg="var(--color-accent-soft)" bg="rgba(34,211,238,0.08)" border="rgba(34,211,238,0.2)">
            {t}
          </Badge>
        ))}
      </div>
    </header>
  );
}
