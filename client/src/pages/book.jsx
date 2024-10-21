import { useEffect } from "react";
import { useParams } from "react-router-dom";

import { useBookById } from "../hooks";
import { Container } from "../components";

const Book = () => {
  const { bookId } = useParams();

  const { book, loading, error } = useBookById(bookId);
  console.log(book);

  useEffect(() => {}, [bookId]);

  return <Container>Book</Container>;
};

export { Book };
