import { useContext } from "react";

import { Container, Row, Col, Card, Button } from "../components";
import { BooksContext, UserContext } from "../contexts";
import { trimText } from "../utils";
import { Link, useNavigate } from "react-router-dom";

const CustomerHome = () => {
  const { user } = useContext(UserContext);
  const { books } = useContext(BooksContext);
  const navigate = useNavigate();

  const handleDetailsClick = (bookId) => {
    navigate(`/books/${bookId}`);
  };

  const bookCards = books?.slice(0, 4).map((book) => {
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
    <Container as="main" className="py-5">
      <Row as="header" className="text-center">
        <h1>Welcome,</h1>
        <span className="fs-2">{user?.username}</span>
      </Row>
      <Row as="section" className="pt-4">
        <h2>Featured Books</h2>
      </Row>
      <Row>{bookCards}</Row>
      <Row>
        <Col className="text-center">
          <Button as={Link} to="/books" variant="warning" size="lg">
            All Books
          </Button>
          <Button
            as={Link}
            to="/customer-books"
            variant="secondary"
            size="lg"
            className="m-2"
          >
            My Books
          </Button>
        </Col>
      </Row>
    </Container>
  );
};

export { CustomerHome };
