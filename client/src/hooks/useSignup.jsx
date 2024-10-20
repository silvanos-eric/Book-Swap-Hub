import { useState, useCallback } from "react";

import { signup } from "../api";

const useSignup = () => {
  const [loading, setLoading] = useState(false);

  const signUpUser = useCallback(async (formData) => {
    setLoading(true);

    try {
      const data = await signup(formData);
      setLoading(false);
      return data; // Return the response data (e.g., user information)
    } catch (error) {
      setLoading(false);
      throw error; // Throw wht error so that the requesting component can handle it
    }
  }, []);

  return { signUpUser, loading };
};

export { useSignup };
