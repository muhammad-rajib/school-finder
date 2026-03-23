export type Teacher = {
  id: string;
  name: string;
  designation: string;
  subject?: string | null;
  qualification?: string | null;
};

export type TeacherCreatePayload = {
  school_id?: string;
  name: string;
  designation: string;
  subject?: string;
  qualification?: string;
  phone?: string;
  joining_date?: string;
};

export type TeacherUpdatePayload = Partial<TeacherCreatePayload>;
