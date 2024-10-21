import { useCallback, useState } from "react";

import { books } from "../api";
import { showErrorToast } from "../utils";

const useBooks = () => {
  const [loading, setLoading] = useState(false);

  const getBooks = useCallback(async () => {
    setLoading(true);

    try {
      const data = await books();
      return data;
    } catch (error) {
      const message = error.message;
      showErrorToast(message);
      console.error(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { getBooks, loading };
};

export { useBooks };
