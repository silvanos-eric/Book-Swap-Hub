import Home from "./pages/Home";
import Books from "./pages/Books";
import Signup from "./pages/UserSignup";
import Login from "./pages/UserLogin";
import ErrorPage from "./pages/ErrorPage";
import Contact from "./pages/Contact";

const routes = [
  {
    path: "/",
    element: <Home />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/books",
    element: <Books />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/signup",
    element: <Signup />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/login",
    element: <Login />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/contact",
    element: <Contact />,
    errorElement: <ErrorPage />,
  },
];

export default routes;
