import { useEffect } from "react";
import { useParams } from "react-router-dom";

import { useBookById } from "../hooks";
import {
  Col,
  Container,
  Row,
  Image,
  ListGroup,
  ButtonGroup,
  Button,
} from "../components";

const Book = () => {
  const { bookId } = useParams();

  const { book, loading, error } = useBookById(bookId);

  useEffect(() => {}, [bookId]);

  return (
    <Container as="main" className="py-5">
      {loading && (
        <Row as="section">
          <p className="lead">Loading....</p>
        </Row>
      )}
      {error && (
        <Row as="section">
          <p className="lead fst-itacli text-danger">{error}</p>
        </Row>
      )}
      {book && (
        <>
          <Row as="section">
            <h1 className="text-center">{book.title}</h1>
          </Row>
          <Row as="section">
            <Image
              src={book.imageUrl}
              height={400}
              className="object-fit-cover"
            />
            <p className="lead">{book.description}</p>
          </Row>
          <Row as="section">
            <h2>Book Details</h2>
            <ListGroup>
              <ListGroup.Item>Author: {book.author}</ListGroup.Item>
              <ListGroup.Item>Status: {book.status}</ListGroup.Item>
              <ListGroup.Item>Price: ${book.price}</ListGroup.Item>
              <ListGroup.Item>Condition: {book.condition}</ListGroup.Item>
            </ListGroup>
          </Row>
          <Row as="section" className="mt-4">
            <ButtonGroup aria-label="Basic example">
              <Button variant="success">Buy</Button>
              <Button variant="secondary">Rent</Button>
            </ButtonGroup>
          </Row>
        </>
      )}
    </Container>
  );
};

export { Book };
