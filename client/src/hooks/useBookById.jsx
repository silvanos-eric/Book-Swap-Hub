import { useEffect, useState } from "react";

import { bookById } from "../api";

const useBookById = (bookId) => {
  const [book, setBook] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!bookId) return;

    const fetchBookData = async () => {
      try {
        const bookData = await bookById(bookId);
        setBook(bookData);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBookData();
  }, [bookId]);

  return { book, isLoading, error };
};

export { useBookById };
