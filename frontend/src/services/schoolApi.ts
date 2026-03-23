import type { School, SchoolListPayload, SchoolSearchParams } from "../features/school/types";
import type { StudentStats } from "../features/student/types";
import type { SchoolImage } from "../features/image/types";
import type { Notice } from "../features/notice/types";
import { buildQuery } from "../shared/utils/query";
import { apiClient } from "./apiClient";
import type { ApiResponse } from "./apiClient";

export async function getSchools(params: SchoolSearchParams = {}) {
  const query = buildQuery(params);
  const path = query ? `/schools?${query}` : "/schools";
  const response = await apiClient.get<ApiResponse<SchoolListPayload>>(path);
  return response.data.data;
}

export async function searchSchools(params: SchoolSearchParams = {}) {
  const query = buildQuery(params);
  const path = query ? `/schools?${query}` : "/schools";
  const response = await apiClient.get<ApiResponse<School[]>>(path);
  return response.data.data;
}

export async function getSchoolDetails(schoolId: string) {
  const response = await apiClient.get<ApiResponse<School>>(`/schools/${schoolId}`);
  return response.data.data;
}

export async function getStudentStats(schoolId: string) {
  const response = await apiClient.get<ApiResponse<StudentStats>>(`/schools/${schoolId}/students`);
  return response.data.data;
}

export async function getSchoolImages(schoolId: string) {
  const response = await apiClient.get<ApiResponse<SchoolImage[]>>(`/schools/${schoolId}/images`);
  return response.data.data;
}

export async function getSchoolNotices(schoolId: string) {
  const response = await apiClient.get<ApiResponse<Notice[]>>(`/schools/${schoolId}/notices`);
  return response.data.data;
}
