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
import { showErrorToast, showSuccessToast } from "../utils";

const Book = () => {
  const { bookId } = useParams();
  const navigate = useNavigate();
  const { book, setBook, loading, error } = useBookById(bookId);
  const { user } = useContext(UserContext);
  const { createTransaction, isLoading: transctionLoading } =
    useCreateTransaction();

  const handleBuyClick = async () => {
    if (!user) {
      return navigate("/login");
    }

    try {
      await createTransaction({
        transactionType: "buy",
        bookId: book.id,
      });
      showSuccessToast("Book purchased successfully");
      setBook({ ...book, status: "bought" });
    } catch (err) {
      showErrorToast(err.message);
    }
  };

  const handleRentClick = async () => {
    if (!user) {
      return navigate("/login");
    }

    try {
      await createTransaction({
        transactionType: "rent",
        bookId: book.id,
      });
      showSuccessToast("Book rented successfully");
      setBook({ ...book, status: "rented" });
    } catch (err) {
      showErrorToast(err.message);
    }
  };

  useEffect(() => {}, [bookId]);

  return (
    <Container as="main" className="py-5" style={{ maxWidth: 600 }}>
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
