import { useState } from "react";

import { useLoginAction } from "../../features/auth/hooks";
import { AppShell } from "../../shared/components/AppShell";
import { ErrorMessage } from "../../shared/components/ErrorMessage";
import { SectionCard } from "../../shared/components/SectionCard";

export function LoginPage() {
  const loginAction = useLoginAction();
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("secret123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await loginAction(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <div className="page">
        <div className="container" style={{ maxWidth: 520 }}>
          <SectionCard title="Login">
            <form className="stack" onSubmit={handleSubmit}>
              <input
                className="input"
                type="email"
                placeholder="Email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
              <input
                className="input"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              <button className="button" disabled={loading} type="submit">
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </form>
            {error ? <ErrorMessage message={error} /> : null}
          </SectionCard>
        </div>
      </div>
    </AppShell>
  );
}
