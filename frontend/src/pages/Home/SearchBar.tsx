import { useEffect, useState } from "react";

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
  onSearch: (filters: SearchFilters) => void;
};

const emptyFilters: SearchFilters = {
  division: "",
  district: "",
  upazila: "",
  union: "",
  name: ""
};

export function SearchBar({ initialValue, loading = false, onSearch }: SearchBarProps) {
  const [filters, setFilters] = useState<SearchFilters>({ ...emptyFilters, ...initialValue });
  const [debouncedName, setDebouncedName] = useState(filters.name);
  const [showAdvanced, setShowAdvanced] = useState(false);

  useEffect(() => {
    setFilters({ ...emptyFilters, ...initialValue });
  }, [initialValue]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedName(filters.name.trim());
    }, 300);

    return () => window.clearTimeout(timer);
  }, [filters.name]);

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

  return (
    <form
      className="search-panel"
      onSubmit={(event) => {
        event.preventDefault();
        onSearch({ ...filters, name: debouncedName });
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

        <button className="button search-submit" disabled={loading} type="submit">
          {loading ? "Searching..." : "Search"}
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
      </div>

      <div className={`advanced-panel ${showAdvanced ? "open" : ""}`}>
        <AdvancedFilters filters={filters} onChange={updateField} />
      </div>
    </form>
  );
}
