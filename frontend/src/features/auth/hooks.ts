import { useNavigate } from "react-router-dom";

import { login } from "../../services/authApi";
import { setAccessToken } from "../../shared/utils/storage";

export function useLoginAction() {
  const navigate = useNavigate();

  return async (email: string, password: string) => {
    const token = await login({ email, password });
    setAccessToken(token.access_token);
    navigate("/dashboard");
  };
}
