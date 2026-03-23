import type { Result } from "../types";
import { EmptyState } from "../../../shared/components/EmptyState";

export function ResultList({ results }: { results: Result[] }) {
  if (!results.length) {
    return <EmptyState title="No results yet" description="Exam result metrics will appear here." />;
  }

  return (
    <div className="grid cols-3">
      {results.map((result) => (
        <article key={result.id} className="card stack">
          <div className="row">
            <h3 style={{ margin: 0 }}>{result.exam_type}</h3>
            <span className="chip">{result.year}</span>
          </div>
          <strong style={{ fontSize: "1.8rem" }}>{result.pass_rate}%</strong>
          <p className="muted" style={{ margin: 0 }}>
            Pass rate for the selected academic year.
          </p>
        </article>
      ))}
    </div>
  );
}
