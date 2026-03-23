import type { PropsWithChildren, ReactNode } from "react";

type SectionCardProps = PropsWithChildren<{
  title?: string;
  action?: ReactNode;
}>;

export function SectionCard({ title, action, children }: SectionCardProps) {
  return (
    <section className="card stack">
      {(title || action) && (
        <div className="row">
          {title ? <h3 className="section-title">{title}</h3> : <span />}
          {action}
        </div>
      )}
      {children}
    </section>
  );
}
