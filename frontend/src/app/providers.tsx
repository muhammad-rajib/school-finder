import { BrowserRouter } from "react-router-dom";

import { AppRoutes } from "./routes";

export function AppProviders() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
