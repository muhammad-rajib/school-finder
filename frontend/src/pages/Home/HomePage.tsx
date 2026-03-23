import { SearchBar } from "./SearchBar";
import { AppShell } from "../../shared/components/AppShell";
import { Container } from "../../shared/components/Container";
import { Hero } from "../../shared/components/Hero";

export function HomePage() {
  return (
    <AppShell>
      <div className="discover-page">
        <Container as="section" className="discover-hero">
          <Hero mode="home" />

          <div className="discover-search">
            <SearchBar />
          </div>
        </Container>
      </div>
    </AppShell>
  );
}
