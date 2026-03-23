import axios from "axios";

import { getAccessToken } from "../shared/utils/storage";

export type ApiResponse<T> = {
  success: boolean;
  data: T;
  message: string;
};

export const apiClient = axios.create({
  baseURL: "http://localhost:8000/api/v1"
});

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.message ?? "Request failed";
    return Promise.reject(new Error(message));
  }
);
