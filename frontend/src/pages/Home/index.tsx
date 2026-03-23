import { useEffect, useState } from "react";

import { AppShell } from "../../shared/components/AppShell";
import { ErrorMessage } from "../../shared/components/ErrorMessage";
import { LoadingBlock } from "../../shared/components/LoadingBlock";
import { SectionCard } from "../../shared/components/SectionCard";
import { SchoolCard } from "../../features/school/components/SchoolCard";
import { SchoolSearchForm } from "../../features/school/components/SchoolSearchForm";
import type { School } from "../../features/school/types";
import { getSchools } from "../../services/schoolApi";

export function HomePage() {
  const [schools, setSchools] = useState<School[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadSchools = async (name?: string) => {
    setLoading(true);
    setError(null);

    try {
      const payload = await getSchools({ name, page: 1, limit: 12 });
      setSchools(payload.schools);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load schools");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadSchools();
  }, []);

  return (
    <AppShell>
      <div className="page">
        <div className="container stack">
          <section className="hero">
            <div className="card stack">
              <span className="chip">Bangladesh School Directory</span>
              <h1>Find schools, compare performance, and explore school profiles.</h1>
              <p>
                SchoolFinder brings overview, teachers, results, notices, and student stats into a
                single searchable experience.
              </p>
              <SchoolSearchForm onSearch={(name) => void loadSchools(name)} />
            </div>
            <div className="card stack">
              <h2 className="section-title">API-ready frontend</h2>
              <p className="muted">
                The architecture is organized by features so we can grow auth, dashboard tools, and
                school management flows without collapsing everything into a single pages folder.
              </p>
            </div>
          </section>

          <SectionCard title="Schools">
            {loading ? <LoadingBlock label="Loading schools..." /> : null}
            {error ? <ErrorMessage message={error} /> : null}
            {!loading && !error ? (
              <div className="grid cols-3">
                {schools.map((school) => (
                  <SchoolCard key={school.id} school={school} />
                ))}
              </div>
            ) : null}
          </SectionCard>
        </div>
      </div>
    </AppShell>
  );
}
