import { useCallback, useEffect, useState } from "react";

import { getBooks } from "../api";

const useBooks = () => {
  const [books, setBooks] = useState([]);
  const [loadingBooks, setLoadingBooks] = useState(false);
  const [errorBooks, setErrorBooks] = useState(null);

  const fetchBooks = useCallback(async () => {
    setErrorBooks(null);
    setLoadingBooks(true);

    try {
      const data = await getBooks(); // Fetch books from API
      setBooks(data);
    } catch (error) {
      const message = error.message;
      setErrorBooks(message);
    } finally {
      setLoadingBooks(false);
    }
  }, []);

  // Fetch all books when the hook is first used
  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  return { loadingBooks, books, errorBooks };
};

export { useBooks };
