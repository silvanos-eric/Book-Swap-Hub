import { useContext } from "react";
import { ErrorMessage, Field, Formik, Form as FormikForm } from "formik";

import {
  Form,
  Button,
  Container,
  Row,
  CustomErroMessage,
  Spinner,
} from "../components";
import { loginValidationSchema } from "../utils";
import { useLogin } from "../hooks";
import { UserContext } from "../contexts";

import "./signup.css";

const Login = () => {
  const { logInUser, loading } = useLogin();
  const { login } = useContext(UserContext);

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const data = await logInUser(values); // Pass form values to custom hook
      login(data);
    } catch (error) {
      console.error(error);
    }
    setSubmitting(false); // Mark the form as not submitting
  };

  return (
    <Container
      className="h-100 d-grid"
      style={{ maxWidth: 600, placeContent: "center" }}
    >
      <Row>
        <h1>Login</h1>
      </Row>
      <Row>
        <Formik
          initialValues={{
            email: "",
            password: "",
          }}
          validationSchema={loginValidationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, errors, touched }) => (
            <Form noValidate as={FormikForm} className="form mx-auto mt-4">
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control
                  as={Field}
                  name="email"
                  type="email"
                  placeholder="e.g. john@example.com"
                  isInvalid={!!errors.email && touched.email}
                  disabled={isSubmitting}
                />
                <ErrorMessage name="email" component={CustomErroMessage} />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  as={Field}
                  name="password"
                  type="password"
                  isInvalid={!!errors.password && touched.password}
                  placeholder="Password"
                  disabled={isSubmitting}
                />
                <ErrorMessage name="password" component={CustomErroMessage} />
              </Form.Group>

              <Button
                disabled={isSubmitting || loading}
                variant="primary"
                type="submit"
              >
                {loading ? (
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                ) : (
                  "Submit"
                )}
              </Button>
            </Form>
          )}
        </Formik>
      </Row>
    </Container>
  );
};

export { Login };
