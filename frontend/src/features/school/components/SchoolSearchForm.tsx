import { useState } from "react";

type SchoolSearchFormProps = {
  initialName?: string;
  onSearch: (name: string) => void;
};

export function SchoolSearchForm({ initialName = "", onSearch }: SchoolSearchFormProps) {
  const [query, setQuery] = useState(initialName);

  return (
    <form
      className="search-form"
      onSubmit={(event) => {
        event.preventDefault();
        onSearch(query);
      }}
    >
      <input
        className="input"
        placeholder="Search by school name"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />
      <button className="button" type="submit">
        Search Schools
      </button>
    </form>
  );
}
