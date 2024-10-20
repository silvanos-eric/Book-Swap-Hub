import { Container, Row, Col } from ".";

const currentYear = new Date().getFullYear();

const Footer = () => {
  return (
    <div className="fixed-bottom bg-body-tertiary ">
      <Container className="p-4">
        <Row>
          <Col className="text-center">
            © {currentYear} Book Swap Hub. All rights reserved.
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export { Footer };
