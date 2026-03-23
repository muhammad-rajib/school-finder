import { Link } from "react-router-dom";
import type { PropsWithChildren } from "react";

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="shell">
      <header className="topbar">
        <div className="container topbar-inner">
          <Link to="/" className="brand">
            SchoolFinder
          </Link>
          <nav className="nav">
            <Link to="/">Home</Link>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/login">Login</Link>
          </nav>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
