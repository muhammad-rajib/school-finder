import { apiClient } from "./apiClient";
import type { ApiResponse } from "./apiClient";
import type { AuthToken, CurrentUser, LoginPayload } from "../features/auth/types";

export async function login(payload: LoginPayload) {
  const response = await apiClient.post<ApiResponse<AuthToken>>("/auth/login", payload);
  return response.data.data;
}

export async function getCurrentUser() {
  const response = await apiClient.get<ApiResponse<CurrentUser>>("/auth/me");
  return response.data.data;
}
