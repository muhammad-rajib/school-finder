import type { Teacher } from "../types";
import { EmptyState } from "../../../shared/components/EmptyState";

export function TeacherList({ teachers }: { teachers: Teacher[] }) {
  if (!teachers.length) {
    return <EmptyState title="No teachers yet" description="Teacher data will appear here." />;
  }

  return (
    <div className="list">
      {teachers.map((teacher) => (
        <article key={teacher.id} className="card stack">
          <div className="row">
            <h3 style={{ margin: 0 }}>{teacher.name}</h3>
            <span className="chip">{teacher.designation}</span>
          </div>
          <div className="meta">
            {teacher.subject ? <span className="chip">{teacher.subject}</span> : null}
            {teacher.qualification ? <span className="chip">{teacher.qualification}</span> : null}
          </div>
        </article>
      ))}
    </div>
  );
}
