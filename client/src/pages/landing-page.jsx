import { useContext } from "react";
import { useNavigate } from "react-router-dom";

import { Container, Button, Row, Col } from "../components";
import data from "../data/landing-page.json";
import "./landing-page.css";
import { UserContext } from "../contexts";

const LandingPage = () => {
  const { user } = useContext(UserContext);
  const navigate = useNavigate();

  const handleCTAClick = () => {
    if (user?.roleNameList?.includes("customer")) {
      navigate("/customer-home");
    } else if (user?.roleNameList?.includes("vendor")) {
      navigate("/vendor-home");
    } else {
      navigate("/signup");
    }
  };

  const sections = data.sections.map((section, index) => (
    <Row
      key={index}
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
          <Button onClick={handleCTAClick} variant="warning" size="lg">
            {data.cta.heading}
          </Button>
        </Col>
      </Row>
      {sections}
    </Container>
  );
};

export { LandingPage };
