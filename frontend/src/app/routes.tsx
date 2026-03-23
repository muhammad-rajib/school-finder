import { Navigate, Route, Routes } from "react-router-dom";

import { DashboardPage } from "../pages/Dashboard";
import { HomePage } from "../pages/Home";
import { LoginPage } from "../pages/Login";
import { SearchResultsPage } from "../pages/SearchResults";
import { SchoolDetailsPage } from "../pages/SchoolDetails";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/results" element={<SearchResultsPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/schools/:schoolId" element={<SchoolDetailsPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
