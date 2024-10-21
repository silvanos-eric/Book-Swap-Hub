import { useEffect, useState } from "react";

import { useBooks } from "../hooks";

const Books = () => {
  const [books, setBooks] = useState([]);
  const { getBooks, loading } = useBooks();

  useEffect(() => {
    const fetchData = async () => {
      const books = await getBooks();
      setBooks(books);
      console.log(books);
    };

    fetchData();
  }, [getBooks]);

  return <>Catalogue</>;
};

export { Books };
