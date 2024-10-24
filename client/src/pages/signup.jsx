import { useContext, useState } from "react";
import { ErrorMessage, Field, Formik, Form as FormikForm } from "formik";
import { useNavigate } from "react-router-dom";

import {
  Form,
  Button,
  Container,
  Row,
  CustomErroMessage,
  Spinner,
} from "../components";
import {
  signupValidationSchema,
  showErrorToast,
  showSuccessToast,
} from "../utils";
import { useSignup } from "../hooks";
import { UserContext } from "../contexts";

import "./signup.css";

const Signup = () => {
  const { signUpUser, loading } = useSignup();
  const { login, user } = useContext(UserContext);
  const navigate = useNavigate();

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const user = await signUpUser(values); // Pass form values to custom hook
      login(user);
      showSuccessToast("Account created successfully");
      if (user.roleNameList.includes("customer")) {
        navigate("/customer-home");
      } else if (user.roleNameList.includes("vendor")) {
        navigate("/vendor-home");
      }
    } catch (error) {
      showErrorToast(error.message);
    }
    setSubmitting(false); // Mark the form as not submitting
  };

  useState(() => {
    if (user?.roleNameList.includes("customer")) {
      navigate("/customer-home");
    } else if (user?.roleNameList.includes("vendor")) {
      navigate("/vendor-home");
    }
  }, [user]);

  return (
    <Container
      className="h-100 d-grid p-5"
      style={{ maxWidth: 600, placeContent: "center" }}
    >
      <Row>
        <h1>Sign Up</h1>
      </Row>
      <Row>
        <Formik
          initialValues={{
            username: "",
            email: "",
            password: "",
            confirmPassword: "",
            role: "customer",
          }}
          validationSchema={signupValidationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, errors, touched }) => (
            <Form noValidate as={FormikForm} className="form mx-auto mt-4">
              <Form.Group className="mb-3" controlId="formBasicUsername">
                <Form.Label>Username</Form.Label>
                <Form.Control
                  as={Field}
                  name="username"
                  type="text"
                  placeholder="e.g. John"
                  isInvalid={!!errors.username && touched.username}
                  disabled={isSubmitting}
                />
                <ErrorMessage name="username" component={CustomErroMessage} />
              </Form.Group>

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

              <Form.Group
                className="mb-3"
                controlId="formBasicPasswordConfirmation"
              >
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control
                  as={Field}
                  name="confirmPassword"
                  type="password"
                  isInvalid={
                    !!errors.confirmPassword && touched.confirmPassword
                  }
                  placeholder="Password"
                  disabled={isSubmitting}
                />
                <ErrorMessage
                  name="confirmPassword"
                  component={CustomErroMessage}
                />
              </Form.Group>

              <Form.Group className="mb-3 d-none" controlId="formBasicRole">
                <Form.Label>Role</Form.Label>
                {["customer", "vendor"].map((role) => (
                  <div key={role} className="mb-3">
                    <Form.Check
                      type="radio"
                      label={role}
                      name="role"
                      id={role}
                      as={Field}
                      value={role}
                      isInvalid={!!errors.role && touched.role}
                      disabled={isSubmitting}
                    />
                  </div>
                ))}
                <ErrorMessage name="role" component={CustomErroMessage} />
              </Form.Group>

              <Button
                disabled={isSubmitting || loading}
                variant="primary"
                type="submit"
              >
                {loading ? (
                  <Spinner animation="border" role="status" size="sm">
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

export { Signup };
