import { useContext } from "react";

import { Col, Container, Row, Tabs, Tab, ListGroup } from "../components";
import { UserContext } from "../contexts";
import { Link } from "react-router-dom";

const CustomerBooks = () => {
  const { user } = useContext(UserContext);

  const purchased = user?.purchasedBooks
    .filter((book) => book.status == "sold")
    .map((book) => (
      <ListGroup.Item as={Link} to={`/books/${book.id}`} key={book.id}>
        {book.title}
      </ListGroup.Item>
    ));

  const rented = user?.purchasedBooks
    .filter((book) => book.status == "rented")
    .map((book) => (
      <ListGroup.Item as={Link} to={`/books/${book.id}`} key={book.id}>
        {book.title}
      </ListGroup.Item>
    ));

  return (
    <Container as="main" className="pt-5">
      <Row as="header">
        <h1 className="text-center">My Books</h1>
      </Row>
      <Tabs
        defaultActiveKey="purchased"
        id="uncontrolled-tab-example"
        className="mb-3"
      >
        <Tab eventKey="purchased" title="Purchased">
          <ListGroup>{purchased}</ListGroup>
        </Tab>
        <Tab eventKey="rented" title="Rented">
          <ListGroup>{rented}</ListGroup>
        </Tab>
      </Tabs>
    </Container>
  );
};

export { CustomerBooks };
