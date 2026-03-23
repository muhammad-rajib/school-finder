import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { searchSchools } from "../../services/schoolApi";
import { AdvancedFilters } from "./AdvancedFilters";

export type SearchFilters = {
  division: string;
  district: string;
  upazila: string;
  union: string;
  name: string;
};

type SearchBarProps = {
  initialValue?: Partial<SearchFilters>;
  loading?: boolean;
  onSearch?: (filters: SearchFilters) => void;
  compact?: boolean;
};

const emptyFilters: SearchFilters = {
  division: "",
  district: "",
  upazila: "",
  union: "",
  name: ""
};

export function SearchBar({
  initialValue,
  loading = false,
  onSearch,
  compact = false
}: SearchBarProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const [filters, setFilters] = useState<SearchFilters>({ ...emptyFilters, ...initialValue });
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setFilters({ ...emptyFilters, ...initialValue });
  }, [initialValue]);

  const updateField = (field: keyof SearchFilters, value: string) => {
    setFilters((current) => {
      if (field === "division") {
        return { ...current, division: value, district: "", upazila: "", union: "" };
      }
      if (field === "district") {
        return { ...current, district: value, upazila: "", union: "" };
      }
      if (field === "upazila") {
        return { ...current, upazila: value, union: "" };
      }
      return { ...current, [field]: value };
    });
  };

  const handleClearFilters = () => {
    setFilters(emptyFilters);
    setShowAdvanced(false);
    onSearch?.(emptyFilters);

    if (location.pathname === "/results") {
      navigate("/results");
      return;
    }

    navigate("/");
  };

  return (
    <form
      className={`search-panel ${compact ? "search-panel-compact" : ""}`}
      onSubmit={async (event) => {
        event.preventDefault();
        const nextFilters = { ...filters, name: filters.name.trim() };
        const params = new URLSearchParams();

        Object.entries(nextFilters).forEach(([key, value]) => {
          if (value.trim()) {
            params.set(key, value.trim());
          }
        });

        setSubmitting(true);
        try {
          await searchSchools(nextFilters);
          onSearch?.(nextFilters);
          navigate({
            pathname: "/results",
            search: params.toString()
          });
        } finally {
          setSubmitting(false);
        }
      }}
    >
      <div className="search-primary">
        <div className="search-field search-field-name">
          <label htmlFor="schoolName">School Name</label>
          <input
            id="schoolName"
            className="input"
            type="text"
            placeholder="Search school by name..."
            value={filters.name}
            onChange={(event) => updateField("name", event.target.value)}
          />
        </div>

        <button className="button search-submit" disabled={loading || submitting} type="submit">
          {loading || submitting ? "Searching..." : "Search"}
        </button>
      </div>

      <div className="search-actions">
        <button
          className="button secondary advanced-toggle"
          type="button"
          onClick={() => setShowAdvanced((current) => !current)}
        >
          {showAdvanced ? "Hide Filters" : "Advanced Filters"}
        </button>
        <button
          className="button secondary clear-filters"
          type="button"
          onClick={handleClearFilters}
        >
          Clear Filters
        </button>
      </div>

      <div className={`advanced-panel ${showAdvanced ? "open" : ""}`}>
        <AdvancedFilters filters={filters} onChange={updateField} />
      </div>
    </form>
  );
}
