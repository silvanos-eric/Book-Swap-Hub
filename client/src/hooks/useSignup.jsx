import { useState } from "react";

import { signup } from "../api";

const useSignup = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState();

  const signupUser = async (formData) => {
    setLoading(true);
    setError(null); // Reset the error state before submission

    try {
      const data = await signup(formData);
      setLoading(false);
      return data; // Return the response data (e.g., user information)
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err; // Throw wht error so that the requesting component can handle it
    }
  };

  return { signupUser, loading, error };
};

export { useSignup };
