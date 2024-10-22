import { useContext, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { useBookById, useCreateTransaction } from "../hooks";
import {
  Container,
  Row,
  Image,
  ListGroup,
  ButtonGroup,
  Button,
} from "../components";
import { UserContext } from "../contexts";

const Book = () => {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const { book, loading, error } = useBookById(bookId);
  const { user } = useContext(UserContext);
  const { createTransaction, isLoading: transctionLoading } =
    useCreateTransaction();

  const handleBuyClick = () => {
    if (!user) {
      navigate("/login");
    }
    createTransaction({
      transactionType: "buy",
      bookId: book.id,
    });
  };

  const handleRentClick = () => {
    if (!user) {
      navigate("/login");
    }
    createTransaction({
      transactionType: "rent",
      bookId: book.id,
    });
  };

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
          {book.status == "available" && (
            <Row as="section" className="mt-4">
              <ButtonGroup aria-label="Basic example">
                <Button
                  disabled={transctionLoading}
                  onClick={handleBuyClick}
                  variant="success"
                >
                  Buy
                </Button>
                <Button
                  disabled={transctionLoading}
                  onClick={handleRentClick}
                  variant="secondary"
                >
                  Rent
                </Button>
              </ButtonGroup>
            </Row>
          )}
          {book.status == "rented" && (
            <p className="lead fst-italic">
              Book is currently rented. Be on the look out for when it is next
              available.
            </p>
          )}
        </>
      )}
    </Container>
  );
};

export { Book };
