import { bangladeshLocations } from "../../features/school/locationData";
import type { SearchFilters } from "./SearchBar";

type AdvancedFiltersProps = {
  filters: SearchFilters;
  onChange: (field: keyof SearchFilters, value: string) => void;
};

export function AdvancedFilters({ filters, onChange }: AdvancedFiltersProps) {
  const divisions = Object.keys(bangladeshLocations);
  const districts = filters.division ? Object.keys(bangladeshLocations[filters.division] ?? {}) : [];
  const upazilas =
    filters.division && filters.district
      ? Object.keys(bangladeshLocations[filters.division]?.[filters.district] ?? {})
      : [];
  const unions =
    filters.division && filters.district && filters.upazila
      ? bangladeshLocations[filters.division]?.[filters.district]?.[filters.upazila] ?? []
      : [];

  return (
    <div className="advanced-grid">
      <div className="search-field">
        <label htmlFor="division">Division</label>
        <select
          id="division"
          className="input"
          value={filters.division}
          onChange={(event) => onChange("division", event.target.value)}
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
          onChange={(event) => onChange("district", event.target.value)}
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
          onChange={(event) => onChange("upazila", event.target.value)}
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
          onChange={(event) => onChange("union", event.target.value)}
        >
          <option value="">Select union</option>
          {unions.map((unionName) => (
            <option key={unionName} value={unionName}>
              {unionName}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
