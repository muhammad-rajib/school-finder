import { useCallback, useState } from "react";

export function useAsync<T>(initialValue: T) {
  const [data, setData] = useState<T>(initialValue);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = useCallback(async (request: () => Promise<T>) => {
    setLoading(true);
    setError(null);

    try {
      const result = await request();
      setData(result);
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong";
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, run, setData };
}
