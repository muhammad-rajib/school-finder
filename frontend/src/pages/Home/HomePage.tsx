import { useNavigate } from "react-router-dom";

import { SearchBar, type SearchFilters } from "./SearchBar";
import { AppShell } from "../../shared/components/AppShell";

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
      <div className="discover-page">
        <section className="discover-hero container">
          <div className="discover-copy">
            <span className="home-kicker">Government Primary School Discovery</span>
            <h1>Find the Right Primary School</h1>
            <p>
              Search and explore detailed information about government primary schools
            </p>
          </div>

          <div className="discover-search">
            <SearchBar onSearch={handleSearch} />
          </div>
        </section>
      </div>
    </AppShell>
  );
}
