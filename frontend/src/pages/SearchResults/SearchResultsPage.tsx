import { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import type { School, SchoolSearchParams } from "../../features/school/types";
import { searchSchools } from "../../services/schoolApi";
import { AppShell } from "../../shared/components/AppShell";
import { EmptyState } from "../../shared/components/EmptyState";
import { ErrorMessage } from "../../shared/components/ErrorMessage";
import { LoadingBlock } from "../../shared/components/LoadingBlock";
import { SearchBar, type SearchFilters } from "../Home/SearchBar";
import { SchoolCard } from "./SchoolCard";

function queryToFilters(search: string): SearchFilters {
  const params = new URLSearchParams(search);

  return {
    division: params.get("division") ?? "",
    district: params.get("district") ?? "",
    upazila: params.get("upazila") ?? "",
    union: params.get("union") ?? "",
    name: params.get("name") ?? ""
  };
}

export function SearchResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [schools, setSchools] = useState<School[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const filters = useMemo(() => queryToFilters(location.search), [location.search]);
  const hasActiveFilters = useMemo(
    () => Object.values(filters).some((value) => value.trim() !== ""),
    [filters]
  );

  useEffect(() => {
    const loadSchools = async (params: SchoolSearchParams) => {
      setLoading(true);
      setError(null);

      try {
        const payload = await searchSchools({ ...params, page: 1, limit: 20 });
        const results = Array.isArray(payload) ? payload : payload.schools;
        setSchools(results);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load schools");
      } finally {
        setLoading(false);
      }
    };

    if (!hasActiveFilters) {
      setSchools([]);
      return;
    }

    void loadSchools(filters);
  }, [filters, hasActiveFilters]);

  const handleSearch = (nextFilters: SearchFilters) => {
    const params = new URLSearchParams();

    Object.entries(nextFilters).forEach(([key, value]) => {
      if (value.trim()) {
        params.set(key, value.trim());
      }
    });

    navigate({
      pathname: "/results",
      search: params.toString()
    });
  };

  return (
    <AppShell>
      <div className="results-page">
        <div className="container results-layout">
          <section className="results-toolbar">
            <div className="results-heading">
              <span className="home-kicker">School Search</span>
              <h1>Search Results</h1>
              <p className="muted">
                {hasActiveFilters
                  ? `${schools.length} school${schools.length === 1 ? "" : "s"} found`
                  : "Start with a school name or open advanced filters"}
              </p>
            </div>
            <SearchBar initialValue={filters} loading={loading} onSearch={handleSearch} />
          </section>

          {loading ? <LoadingBlock label="Searching..." /> : null}
          {error ? <ErrorMessage message={error} /> : null}

          {!loading && !error && hasActiveFilters && schools.length > 0 ? (
            <section className="results-list">
              {schools.map((school) => (
                <SchoolCard key={school.id} school={school} />
              ))}
            </section>
          ) : null}

          {!loading && !error && hasActiveFilters && schools.length === 0 ? (
            <EmptyState
              title="No schools found"
              description="Try a broader school name or adjust the advanced filters."
            />
          ) : null}
        </div>
      </div>
    </AppShell>
  );
}
