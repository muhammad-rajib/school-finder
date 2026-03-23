import { Link } from "react-router-dom";

import type { School } from "../types";

export function SchoolCard({ school }: { school: School }) {
  return (
    <article className="card stack">
      <div className="row">
        <div>
          <h3 style={{ margin: 0 }}>{school.name}</h3>
          <p className="muted" style={{ margin: "6px 0 0" }}>
            EMIS {school.emis_code}
          </p>
        </div>
        <span className="chip">{school.country_code}</span>
      </div>
      <div className="meta">
        {school.division ? <span className="chip">{school.division}</span> : null}
        {school.district ? <span className="chip">{school.district}</span> : null}
        {school.upazila ? <span className="chip">{school.upazila}</span> : null}
      </div>
      <p className="muted">{school.description ?? "School profile details will appear here."}</p>
      <Link className="button" to={`/schools/${school.id}`}>
        View Details
      </Link>
    </article>
  );
}
