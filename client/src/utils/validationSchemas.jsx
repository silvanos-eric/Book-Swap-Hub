import * as Yup from "yup";

const signupValidationSchema = Yup.object({
  username: Yup.string()
    .min(3, "Username cannot be shorter than 3 characters")
    .max(15, "Username must be at most 15 characters")
    .required("Username is required"),
  email: Yup.string().email().required("Email is required"),
  password: Yup.string()
    .min(8, "Password must be at least 8 characters")
    .required("Password is required"),
  confirmPassword: Yup.string("Confirm Password is required")
    .oneOf([Yup.ref("password"), null], "Passwords must match")
    .required("Confirm Password is required"),
  role: Yup.string().required("Role is required"),
});

const loginValidationSchema = Yup.object({
  email: Yup.string().email().required("Email is required"),
  password: Yup.string()
    .min(8, "Password must be at least 8 characters")
    .required("Password is required"),
});

export { signupValidationSchema, loginValidationSchema };
