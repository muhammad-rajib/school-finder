import { Link } from "react-router-dom";

import type { School } from "../../../features/school/types";

export function SchoolCard({ school }: { school: School }) {
  const location = [school.division, school.district].filter(Boolean).join(", ");

  return (
    <article className="result-card">
      <div className="result-card-main">
        <div className="result-card-body">
          <h2>{school.name}</h2>
          <p className="result-location">{location || "Location not available"}</p>
        </div>
        <div className="result-card-actions">
          <Link className="button" to={`/schools/${school.id}`}>
            View
          </Link>
        </div>
      </div>
    </article>
  );
}
