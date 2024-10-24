import { createContext, useEffect, useState } from "react";
import PropTypes from "prop-types";

import { useBooks } from "../hooks";

const BooksContext = createContext();

const BooksProvider = ({ children }) => {
  const [books, setBooks] = useState();
  const { getBooks, loading, error } = useBooks();

  // Automatically fetch data when the context provider is mounted
  useEffect(() => {
    const fetchBooks = async () => {
      const data = await getBooks();
      setBooks(data);
    };

    fetchBooks();
  }, [getBooks]);

  return (
    <BooksContext.Provider value={{ books, loading, error }}>
      {children}
    </BooksContext.Provider>
  );
};

BooksProvider.propTypes = {
  children: PropTypes.node,
};

export { BooksProvider, BooksContext };
