import { useCallback, useState } from "react";

import { checkSession } from "../api";

const useCheckSession = () => {
  const [loading, setLoading] = useState(true);

  const checkUserSession = useCallback(async () => {
    try {
      const user = await checkSession();
      setLoading(false);
      return user;
    } catch (error) {
      setLoading(false);
      throw error;
    }
  }, []);

  return {
    checkUserSession,
    loading,
  };
};

export { useCheckSession };
