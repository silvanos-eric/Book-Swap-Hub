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
  VendorBooks,
  CustomerBooks,
} from "./pages";

import { UserProvider } from "./contexts";

const routes = [
  {
    path: "/",
    element: (
      <UserProvider>
        <Root />
      </UserProvider>
    ),
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <LandingPage />,
      },
      {
        path: "customer-home",
        element: <CustomerHome />,
      },
      {
        path: "vendor-home",
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
