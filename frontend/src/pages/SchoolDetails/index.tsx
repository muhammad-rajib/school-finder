import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { ResultList } from "../../features/result/components/ResultList";
import { TeacherList } from "../../features/teacher/components/TeacherList";
import type { Result } from "../../features/result/types";
import type { School } from "../../features/school/types";
import type { Teacher } from "../../features/teacher/types";
import { AppShell } from "../../shared/components/AppShell";
import { EmptyState } from "../../shared/components/EmptyState";
import { ErrorMessage } from "../../shared/components/ErrorMessage";
import { LoadingBlock } from "../../shared/components/LoadingBlock";
import { SectionCard } from "../../shared/components/SectionCard";
import { getResultsBySchool } from "../../services/resultApi";
import { getSchoolDetails } from "../../services/schoolApi";
import { getTeachersBySchool } from "../../services/teacherApi";

type ActiveTab = "overview" | "teachers" | "results";

export function SchoolDetailsPage() {
  const { schoolId = "" } = useParams();
  const [activeTab, setActiveTab] = useState<ActiveTab>("overview");
  const [school, setSchool] = useState<School | null>(null);
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);

      try {
        const [schoolData, teacherData, resultData] = await Promise.all([
          getSchoolDetails(schoolId),
          getTeachersBySchool(schoolId),
          getResultsBySchool(schoolId)
        ]);
        setSchool(schoolData);
        setTeachers(teacherData);
        setResults(resultData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load school details");
      } finally {
        setLoading(false);
      }
    };

    if (schoolId) {
      void load();
    }
  }, [schoolId]);

  const renderTabContent = () => {
    if (!school) {
      return <EmptyState title="School not found" description="We could not load this school profile." />;
    }

    if (activeTab === "teachers") {
      return <TeacherList teachers={teachers} />;
    }

    if (activeTab === "results") {
      return <ResultList results={results} />;
    }

    return (
      <div className="grid cols-2">
        <SectionCard title="About">
          <p className="muted">{school.description ?? "No description available yet."}</p>
          <div className="meta">
            {school.phone ? <span className="chip">{school.phone}</span> : null}
            {school.email ? <span className="chip">{school.email}</span> : null}
            {school.website ? <span className="chip">{school.website}</span> : null}
          </div>
        </SectionCard>
        <SectionCard title="Facilities">
          <div className="meta">
            <span className="chip">{school.total_students} students</span>
            <span className="chip">{school.total_teachers} teachers</span>
            <span className="chip">{school.total_classrooms} classrooms</span>
            <span className="chip">
              Electricity: {school.has_electricity ? "Available" : "Not available"}
            </span>
            <span className="chip">Water: {school.has_water ? "Available" : "Not available"}</span>
          </div>
        </SectionCard>
      </div>
    );
  };

  return (
    <AppShell>
      <div className="page">
        <div className="container stack">
          {loading ? <LoadingBlock label="Loading school profile..." /> : null}
          {error ? <ErrorMessage message={error} /> : null}
          {!loading && !error && school ? (
            <>
              <section className="card stack">
                <span className="chip">{school.country_code}</span>
                <h1 style={{ margin: 0 }}>{school.name}</h1>
                <p className="muted" style={{ margin: 0 }}>
                  {school.address ?? "Address not available"}
                </p>
                <div className="tabs">
                  {(["overview", "teachers", "results"] as ActiveTab[]).map((tab) => (
                    <button
                      key={tab}
                      className={`tab ${activeTab === tab ? "active" : ""}`}
                      type="button"
                      onClick={() => setActiveTab(tab)}
                    >
                      {tab}
                    </button>
                  ))}
                </div>
              </section>
              {renderTabContent()}
            </>
          ) : null}
        </div>
      </div>
    </AppShell>
  );
}
