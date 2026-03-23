import type { Teacher, TeacherCreatePayload, TeacherUpdatePayload } from "../features/teacher/types";
import { apiClient } from "./apiClient";
import type { ApiResponse } from "./apiClient";

export async function getTeachersBySchool(schoolId: string) {
  const response = await apiClient.get<ApiResponse<Teacher[]>>(`/schools/${schoolId}/teachers`);
  return response.data.data;
}

export async function createTeacher(payload: TeacherCreatePayload) {
  const response = await apiClient.post<ApiResponse<Teacher>>("/teachers", payload);
  return response.data.data;
}

export async function updateTeacher(teacherId: string, payload: TeacherUpdatePayload) {
  const response = await apiClient.put<ApiResponse<Teacher>>(`/teachers/${teacherId}`, payload);
  return response.data.data;
}

export async function deleteTeacher(teacherId: string) {
  const response = await apiClient.delete<ApiResponse<{ message: string }>>(`/teachers/${teacherId}`);
  return response.data.data;
}
