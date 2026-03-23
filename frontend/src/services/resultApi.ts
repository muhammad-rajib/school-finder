import type { Result, ResultCreatePayload, ResultUpdatePayload } from "../features/result/types";
import { apiClient } from "./apiClient";
import type { ApiResponse } from "./apiClient";

export async function getResultsBySchool(schoolId: string) {
  const response = await apiClient.get<ApiResponse<Result[]>>(`/schools/${schoolId}/results`);
  return response.data.data;
}

export async function createResult(payload: ResultCreatePayload) {
  const response = await apiClient.post<ApiResponse<Result>>("/results", payload);
  return response.data.data;
}

export async function updateResult(resultId: string, payload: ResultUpdatePayload) {
  const response = await apiClient.put<ApiResponse<Result>>(`/results/${resultId}`, payload);
  return response.data.data;
}

export async function deleteResult(resultId: string) {
  const response = await apiClient.delete<ApiResponse<{ message: string }>>(`/results/${resultId}`);
  return response.data.data;
}
