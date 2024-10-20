import { useState } from "react";
import { login } from "../api";

const useLogin = () => {
  const [loading, setLoading] = useState(false);

  const logInUser = async () => {
    try {
      setLoading(true);
      const user = await login();
      setLoading(false);
      return user;
    } catch (error) {
      setLoading(false);
      throw new Error(error);
    }
  };

  return {
    logInUser,
    loading,
  };
};

export { useLogin };
