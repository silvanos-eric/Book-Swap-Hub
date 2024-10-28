import { createContext } from "react";
import PropTypes from "prop-types";

import { useBooks } from "../hooks";

const BooksContext = createContext();

const BooksProvider = ({ children }) => {
  const { loadingBooks, books, errorBooks } = useBooks();

  return (
    <BooksContext.Provider value={{ books, loadingBooks, errorBooks }}>
      {children}
    </BooksContext.Provider>
  );
};

BooksProvider.propTypes = {
  children: PropTypes.node,
};

export { BooksProvider, BooksContext };
