import {
  LandingPage,
  Root,
  VendorHome,
  CustomerHome,
  ErrorPage,
  Books,
  Book,
  Signup,
  Login,
  Contact,
} from "./pages";

const routes = [
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <LandingPage />,
      },
      {
        path: "customer",
        element: <CustomerHome />,
      },
      {
        path: "vendor",
        element: <VendorHome />,
      },
      {
        path: "books",
        element: <Books />,
      },
      {
        path: "book",
        element: <Book />,
      },
      {
        path: "signup",
        element: <Signup />,
      },
      {
        path: "login",
        element: <Login />,
      },
      {
        path: "contact",
        element: <Contact />,
      },
    ],
  },
];

export default routes;
