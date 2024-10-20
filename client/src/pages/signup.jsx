import { Form, Button, Container, Row } from "@components";

import "./signup.css";

const Signup = () => {
  return (
    <Container
      className="h-100 d-grid"
      style={{ maxWidth: 600, placeContent: "center" }}
    >
      <Row>
        <h1>Sign Up</h1>
      </Row>
      <Row>
        <Form className="form mx-auto mt-4">
          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="e.g. John" required />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control
              type="email"
              placeholder="e.g. john@example.com"
              required
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Password" required />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicRole">
            <Form.Label>Role</Form.Label>
            {["customer", "role"].map((role) => (
              <div key={role} className="mb-3">
                <Form.Check
                  name="role"
                  type="radio"
                  id={role}
                  label={role}
                  required
                />
              </div>
            ))}
          </Form.Group>

          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Row>
    </Container>
  );
};

export { Signup };
