export type LoginPayload = {
  email: string;
  password: string;
};

export type AuthToken = {
  access_token: string;
  token_type: string;
};

export type CurrentUser = {
  id: string;
  name: string;
  email: string;
  role: string;
  school_id?: string | null;
  is_active: boolean;
};
