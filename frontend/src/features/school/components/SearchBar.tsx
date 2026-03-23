import { useEffect, useMemo, useState } from "react";

import { bangladeshLocations } from "../locationData";

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
  const [filters, setFilters] = useState<SearchFilters>({
    ...emptyFilters,
    ...initialValue
  });
  const [debouncedName, setDebouncedName] = useState(filters.name);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedName(filters.name.trim());
    }, 300);

    return () => window.clearTimeout(timer);
  }, [filters.name]);

  useEffect(() => {
    setFilters({
      ...emptyFilters,
      ...initialValue
    });
  }, [initialValue]);

  const divisions = useMemo(() => Object.keys(bangladeshLocations), []);
  const districts = filters.division ? Object.keys(bangladeshLocations[filters.division] ?? {}) : [];
  const upazilas =
    filters.division && filters.district
      ? Object.keys(bangladeshLocations[filters.division]?.[filters.district] ?? {})
      : [];
  const unions =
    filters.division && filters.district && filters.upazila
      ? bangladeshLocations[filters.division]?.[filters.district]?.[filters.upazila] ?? []
      : [];

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
      className="travel-search"
      onSubmit={(event) => {
        event.preventDefault();
        onSearch({ ...filters, name: debouncedName });
      }}
    >
      <div className="search-field">
        <label htmlFor="division">Division</label>
        <select
          id="division"
          className="input"
          value={filters.division}
          onChange={(event) => updateField("division", event.target.value)}
        >
          <option value="">Select division</option>
          {divisions.map((division) => (
            <option key={division} value={division}>
              {division}
            </option>
          ))}
        </select>
      </div>

      <div className="search-field">
        <label htmlFor="district">District</label>
        <select
          id="district"
          className="input"
          disabled={!filters.division}
          value={filters.district}
          onChange={(event) => updateField("district", event.target.value)}
        >
          <option value="">Select district</option>
          {districts.map((district) => (
            <option key={district} value={district}>
              {district}
            </option>
          ))}
        </select>
      </div>

      <div className="search-field">
        <label htmlFor="upazila">Upazila</label>
        <select
          id="upazila"
          className="input"
          disabled={!filters.district}
          value={filters.upazila}
          onChange={(event) => updateField("upazila", event.target.value)}
        >
          <option value="">Select upazila</option>
          {upazilas.map((upazila) => (
            <option key={upazila} value={upazila}>
              {upazila}
            </option>
          ))}
        </select>
      </div>

      <div className="search-field">
        <label htmlFor="union">Union</label>
        <select
          id="union"
          className="input"
          disabled={!filters.upazila}
          value={filters.union}
          onChange={(event) => updateField("union", event.target.value)}
        >
          <option value="">Select union</option>
          {unions.map((unionName) => (
            <option key={unionName} value={unionName}>
              {unionName}
            </option>
          ))}
        </select>
      </div>

      <div className="search-field search-field-name">
        <label htmlFor="schoolName">School name</label>
        <input
          id="schoolName"
          className="input"
          type="text"
          placeholder="Start typing a school name"
          value={filters.name}
          onChange={(event) => updateField("name", event.target.value)}
        />
      </div>

      <button className="button search-submit" disabled={loading} type="submit">
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}
