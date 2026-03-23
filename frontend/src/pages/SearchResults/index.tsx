import { useEffect, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { SearchBar, type SearchFilters } from "../../features/school/components/SearchBar";
import { SchoolCard } from "../../features/school/components/SchoolCard";
import type { School, SchoolSearchParams } from "../../features/school/types";
import { searchSchools } from "../../services/schoolApi";
import { AppShell } from "../../shared/components/AppShell";
import { EmptyState } from "../../shared/components/EmptyState";
import { ErrorMessage } from "../../shared/components/ErrorMessage";
import { LoadingBlock } from "../../shared/components/LoadingBlock";

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
        const payload = await searchSchools({ ...params, page: 1, limit: 12 });
        setSchools(payload.schools);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load schools");
      } finally {
        setLoading(false);
      }
    };

    if (!hasActiveFilters) {
      setSchools([]);
      setLoading(false);
      return;
    }

    void loadSchools(filters);
  }, [filters, hasActiveFilters]);

  const resultsLabel = hasActiveFilters
    ? `Found ${schools.length} school${schools.length === 1 ? "" : "s"}`
    : "Use the search filters to find schools";

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
      <div className="home-modern">
        <header className="home-navbar container">
          <Link to="/" className="brand home-brand">
            SchoolFinder
          </Link>
          <Link to="/login" className="button secondary home-login">
            Login
          </Link>
        </header>

        <main className="page">
          <div className="container home-stack">
            <section className="results-header stack">
              <div className="stack" style={{ gap: 8 }}>
                <span className="home-kicker">School Search Results</span>
                <h1 style={{ margin: 0 }}>Explore matching schools</h1>
                <p className="muted" style={{ margin: 0 }}>
                  {resultsLabel}
                </p>
              </div>
              <div className="home-search-shell">
                <SearchBar initialValue={filters} loading={loading} onSearch={handleSearch} />
              </div>
            </section>

            {loading ? <LoadingBlock label="Searching schools..." /> : null}
            {error ? <ErrorMessage message={error} /> : null}

            {!loading && !error && hasActiveFilters && schools.length > 0 ? (
              <section className="results-grid">
                {schools.map((school) => (
                  <SchoolCard key={school.id} school={school} />
                ))}
              </section>
            ) : null}

            {!loading && !error && hasActiveFilters && schools.length === 0 ? (
              <EmptyState
                title="No schools found"
                description="Try another location combination or broaden the school name search."
              />
            ) : null}

            {!loading && !error && !hasActiveFilters ? (
              <EmptyState
                title="Start a search"
                description="Choose a location or type a school name to fetch live results."
              />
            ) : null}
          </div>
        </main>
      </div>
    </AppShell>
  );
}
