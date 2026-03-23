import { SearchBar } from "./SearchBar";
import { AppShell } from "../../shared/components/AppShell";

export function HomePage() {
  return (
    <AppShell>
      <div className="discover-page">
        <section className="discover-hero container">
          <div className="discover-copy">
            <span className="home-kicker">School Search</span>
            <h1>Discover Primary Schools Near You</h1>
            <p>Search and explore detailed school information</p>
          </div>

          <div className="discover-search">
            <SearchBar />
          </div>
        </section>
      </div>
    </AppShell>
  );
}
