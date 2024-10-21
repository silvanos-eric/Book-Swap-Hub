import { useCallback, useState } from "react";

import { books } from "../api";
import { showErrorToast } from "../utils";

const useBooks = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getBooks = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await books(); // Fetch books from API
      return data;
    } catch (error) {
      const message = error.message;
      setError(message);
      showErrorToast(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { getBooks, loading, error };
};

export { useBooks };
