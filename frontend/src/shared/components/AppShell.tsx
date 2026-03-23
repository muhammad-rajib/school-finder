import type { PropsWithChildren } from "react";

import { Navbar } from "./Navbar";
import { ScrollToTopButton } from "./ScrollToTopButton";

export function AppShell({ children }: PropsWithChildren) {
  return (
    <div className="shell">
      <Navbar />
      <main>{children}</main>
      <ScrollToTopButton />
    </div>
  );
}
