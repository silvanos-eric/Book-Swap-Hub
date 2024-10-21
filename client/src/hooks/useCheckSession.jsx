import { useCallback, useState } from "react";

import { checkSession } from "../api";

const useCheckSession = () => {
  const [loading, setLoading] = useState(false);

  const checkUserSession = useCallback(async () => {
    setLoading(false);

    try {
      const user = await checkSession();
      return user;
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    checkUserSession,
    loading,
  };
};

export { useCheckSession };
