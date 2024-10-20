import { Link } from "react-router-dom";

import { Container, Button, Row, Col } from "@components";
import data from "@data/landing-page.json";
import "./landing-page.css";

const LandingPage = () => {
  const sections = data.sections.map((section, i) => (
    <Row
      key={i}
      as="section"
      className="pt-5 mx-auto"
      style={{ maxWidth: "800px" }}
    >
      <Col>
        <h2>{section.heading}</h2>
        <p className="lead">{section.body}</p>
      </Col>
    </Row>
  ));

  return (
    <Container as="main" className="py-5 text-center">
      <Row as="header" className="hero">
        <Col className="d-flex flex-column justify-content-center p-0">
          <div className="hero-content">
            <h1 style={{ maxWidth: "600px" }} className="mx-auto">
              {data.headline}
            </h1>
            <h2 style={{ maxWidth: "800px" }} className="mx-auto">
              {data.subheadline}
            </h2>
          </div>
        </Col>
      </Row>
      <Row as="section" className="pt-5">
        <Col>
          <Button as={Link} to="/signup" variant="warning">
            {data.cta.heading}
          </Button>
        </Col>
      </Row>
      {sections}
    </Container>
  );
};

export { LandingPage };
