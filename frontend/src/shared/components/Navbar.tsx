import { Link } from "react-router-dom";

import { getAccessToken } from "../utils/storage";

export function Navbar() {
  const isLoggedIn = Boolean(getAccessToken());

  return (
    <header className="topbar">
      <div className="container topbar-inner">
        <Link to="/" className="brand">
          SchoolFinder
        </Link>
        <Link to={isLoggedIn ? "/dashboard" : "/login"} className="button secondary nav-cta">
          {isLoggedIn ? "Dashboard" : "Login"}
        </Link>
      </div>
    </header>
  );
}
