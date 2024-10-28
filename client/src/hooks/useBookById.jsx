import { useContext, useEffect, useState } from "react";

import { getBook } from "../api";
import { BooksContext } from "../contexts";

const useBookById = (bookId) => {
  const [book, setBook] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const { books } = useContext(BooksContext);

  useEffect(() => {
    if (!bookId) return;

    const fetchBookData = async () => {
      try {
        const bookData = await getBook(bookId);
        setBook(bookData);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    if (books.length < 1) {
      fetchBookData();
    } else {
      setBook(() => books.find((book) => book.id == bookId));
    }
  }, [bookId, books]);

  return { book, setBook, isLoading, error };
};

export { useBookById };
