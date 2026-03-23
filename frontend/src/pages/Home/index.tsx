import { Link, useNavigate } from "react-router-dom";

import { AppShell } from "../../shared/components/AppShell";
import { SearchBar, type SearchFilters } from "../../features/school/components/SearchBar";

export function HomePage() {
  const navigate = useNavigate();

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
                <SearchBar onSearch={handleSearch} />
              </div>
            </section>

            <section className="home-preview card">
              <div className="stack">
                <h2 className="section-title">Search across Bangladesh</h2>
                <p className="muted" style={{ margin: 0 }}>
                  Filter by division, district, upazila, union, and school name to quickly find
                  the right school profile. Results open on a dedicated page with live backend
                  data.
                </p>
                <div className="meta">
                  <span className="chip">Responsive search</span>
                  <span className="chip">Backend API connected</span>
                  <span className="chip">Fast detail navigation</span>
                </div>
              </div>
            </section>
          </div>
        </main>
      </div>
    </AppShell>
  );
}
