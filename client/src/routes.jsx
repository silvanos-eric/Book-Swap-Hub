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

import { BooksProvider, UserProvider } from "./contexts";

const routes = [
  {
    path: "/",
    element: (
      <BooksProvider>
        <UserProvider>
          <Root />
        </UserProvider>
      </BooksProvider>
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
        path: "books/:bookId",
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
