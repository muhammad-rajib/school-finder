export type School = {
  id: string;
  emis_code: string;
  name: string;
  country_code: string;
  division?: string | null;
  district?: string | null;
  upazila?: string | null;
  union?: string | null;
  address?: string | null;
  description?: string | null;
  phone?: string | null;
  email?: string | null;
  website?: string | null;
  established_year?: number | null;
  total_students: number;
  total_teachers: number;
  total_classrooms: number;
  has_electricity: boolean;
  has_water: boolean;
  created_at: string;
};

export type SchoolListPayload = {
  schools: School[];
  page: number;
  limit: number;
};

export type SchoolSearchParams = {
  name?: string;
  division?: string;
  district?: string;
  upazila?: string;
  union?: string;
  page?: number;
  limit?: number;
};
