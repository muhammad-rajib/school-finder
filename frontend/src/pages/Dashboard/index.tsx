import { Link } from "react-router-dom";

import { SectionCard } from "../../shared/components/SectionCard";

export function DashboardPage() {
  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="brand">SchoolFinder Admin</div>
        <nav className="nav">
          <Link to="/dashboard">Overview</Link>
          <Link to="/">School Search</Link>
          <Link to="/login">Account</Link>
        </nav>
      </aside>

      <main className="dashboard-main">
        <div className="stack">
          <SectionCard title="Dashboard">
            <p className="muted">
              This layout is ready for principal and admin tools like teacher CRUD, result updates,
              notices, and media management.
            </p>
          </SectionCard>
          <div className="grid cols-3">
            <SectionCard title="Teachers">
              <p className="muted">Manage staff assignments and academic roles.</p>
            </SectionCard>
            <SectionCard title="Results">
              <p className="muted">Publish and edit annual exam performance data.</p>
            </SectionCard>
            <SectionCard title="Notices">
              <p className="muted">Share school updates for guardians and students.</p>
            </SectionCard>
          </div>
        </div>
      </main>
    </div>
  );
}
