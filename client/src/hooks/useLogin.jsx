import { useState, useCallback } from "react";

import { login } from "../api";

const useLogin = () => {
  const [loading, setLoading] = useState(false);

  const logInUser = useCallback(async (formData) => {
    setLoading(true);

    try {
      const user = await login(formData);
      setLoading(false);
      return user;
    } catch (error) {
      setLoading(false);
      throw new Error(error);
    }
  }, []);

  return {
    logInUser,
    loading,
  };
};

export { useLogin };
