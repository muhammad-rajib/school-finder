import type { Notice } from "../features/notice/types";
import { apiClient } from "./apiClient";
import type { ApiResponse } from "./apiClient";

export async function getNoticesBySchool(schoolId: string) {
  const response = await apiClient.get<ApiResponse<Notice[]>>(`/schools/${schoolId}/notices`);
  return response.data.data;
}
