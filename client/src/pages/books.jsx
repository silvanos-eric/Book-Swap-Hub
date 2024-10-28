import { useContext } from "react";
import { useNavigate } from "react-router-dom";

import { Container, Row, Col, Spinner, Card, Button } from "../components";
import { BooksContext } from "../contexts";
import { trimText } from "../utils";

const Books = () => {
  const { books, loadingBooks, errorBooks } = useContext(BooksContext);
  const navigate = useNavigate();

  const handleDetailsClick = (bookId) => {
    navigate(`/books/${bookId}`);
  };

  const variants = [
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "dark",
  ];
  const spinners = variants.map((variant) => (
    <Spinner key={variant} variant={variant} animation="grow" />
  ));

  const bookCards = books?.map((book) => {
    const trimmedDescription = trimText(book.description, 50);

    return (
      <Col key={book.id} sm={6} md={5} lg={4} xl={3} className="mb-4">
        <Card>
          <Card.Img
            variant="top"
            src={book.imageUrl}
            className="object-fit-cover"
            style={{
              height: 250,
            }}
          />
          <Card.Body>
            <Card.Title>{book.title}</Card.Title>
            <Card.Text>{trimmedDescription}</Card.Text>
            <Button
              onClick={() => {
                handleDetailsClick(book.id);
              }}
              variant="primary"
            >
              Details
            </Button>
          </Card.Body>
        </Card>
      </Col>
    );
  });

  return (
    <Container as="main" className="py-5 d-flex flex-column h-100">
      <Row as="header">
        <Col>
          <h1 className="text-center">Catalogue</h1>
        </Col>
      </Row>
      {(errorBooks || loadingBooks) && (
        <Row
          as="section"
          className="text-center flex-grow-1 d-grid"
          style={{ placeContent: "center" }}
        >
          {loadingBooks && <Col>{spinners}</Col>}
          {errorBooks && (
            <Col>
              <p className="lead text-danger fst-italic">{errorBooks}</p>
            </Col>
          )}
        </Row>
      )}
      {books && (
        <Row as="section" className="mt-5 justify-content-center">
          {bookCards}
        </Row>
      )}
    </Container>
  );
};

export { Books };
