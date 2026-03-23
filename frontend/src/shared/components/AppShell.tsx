import type { PropsWithChildren } from "react";

import { Navbar } from "./Navbar";

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="shell">
      <Navbar />
      <main>{children}</main>
    </div>
  );
}
