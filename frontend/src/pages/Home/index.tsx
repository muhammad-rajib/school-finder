import { useEffect, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { AppShell } from "../../shared/components/AppShell";
import { ErrorMessage } from "../../shared/components/ErrorMessage";
import { LoadingBlock } from "../../shared/components/LoadingBlock";
import { SchoolCard } from "../../features/school/components/SchoolCard";
import { SearchBar, type SearchFilters } from "../../features/school/components/SearchBar";
import type { School, SchoolSearchParams } from "../../features/school/types";
import { getSchools } from "../../services/schoolApi";

export function HomePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [schools, setSchools] = useState<School[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const filters = useMemo(() => {
    const params = new URLSearchParams(location.search);

    return {
      division: params.get("division") ?? "",
      district: params.get("district") ?? "",
      upazila: params.get("upazila") ?? "",
      union: params.get("union") ?? "",
      name: params.get("name") ?? ""
    };
  }, [location.search]);

  const hasActiveFilters = useMemo(
    () => Object.values(filters).some((value) => value.trim() !== ""),
    [filters]
  );

  const loadSchools = async (params: SchoolSearchParams) => {
    setLoading(true);
    setError(null);

    try {
      const payload = await getSchools({ ...params, page: 1, limit: 12 });
      setSchools(payload.schools);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load schools");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!hasActiveFilters) {
      setSchools([]);
      setLoading(false);
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
            <section className="home-hero">
              <div className="home-copy">
                <span className="home-kicker">Bangladesh School Search</span>
                <h1>Find Primary Schools</h1>
                <p>Search schools by location and name</p>
              </div>

              <div className="home-search-shell">
                <SearchBar initialValue={filters} loading={loading} onSearch={handleSearch} />
              </div>
            </section>

            <section className="home-results">
              <div className="row">
                <div>
                  <h2 className="section-title">Search Results</h2>
                  <p className="muted" style={{ margin: "6px 0 0" }}>
                    {hasActiveFilters
                      ? `Found ${schools.length} school${schools.length === 1 ? "" : "s"} for your filters`
                      : "Choose a location or type a school name to explore schools"}
                  </p>
                </div>
              </div>

              {loading ? <LoadingBlock label="Searching schools..." /> : null}
              {error ? <ErrorMessage message={error} /> : null}

              {!loading && !error && hasActiveFilters && schools.length > 0 ? (
                <div className="grid cols-3">
                  {schools.map((school) => (
                    <SchoolCard key={school.id} school={school} />
                  ))}
                </div>
              ) : null}

              {!loading && !error && hasActiveFilters && schools.length === 0 ? (
                <div className="empty-state">
                  <h3>No schools found</h3>
                  <p>Try a different division, district, or school name.</p>
                </div>
              ) : null}
            </section>
          </div>
        </main>
      </div>
    </AppShell>
  );
}
