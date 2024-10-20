import {
  LandingPage,
  Root,
  VendorHome,
  CustomerHome,
  ErrorPage,
  Catalogue,
  Book,
  Signup,
  Login,
  Contact,
  VendorBooks,
  CustomerBooks,
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
        path: "catalogue",
        element: <Catalogue />,
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
      {
        path: "vendor-books",
        element: <VendorBooks />,
      },
      {
        path: "customer-books",
        element: <CustomerBooks />,
      },
    ],
  },
];

export default routes;
