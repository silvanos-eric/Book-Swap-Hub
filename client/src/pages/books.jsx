import { useContext, useEffect, useState } from "react";

import { Container, Row, Col, Spinner } from "../components";
import { BooksContext } from "../contexts";

const Books = () => {
  const { books, loading, error } = useContext(BooksContext);

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

  return (
    <Container as="main" className="py-5 d-flex flex-column h-100">
      <Row as="header">
        <Col>
          <h1 className="text-center">Catalogue</h1>
        </Col>
      </Row>
      <Row
        className="text-center flex-grow-1 d-grid"
        style={{ placeContent: "center" }}
      >
        {loading && <Col>{spinners}</Col>}
        {error && <Col></Col>}
      </Row>
    </Container>
  );
};

export { Books };
