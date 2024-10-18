import NavBar from "../components/Navbar"
import Footer from "../components/Footer";
import { useRouteError } from "react-router-dom";

function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <>
      <header>
        <NavBar />
      </header>
      <main>
        <h1>Whoops! Something went wrong!</h1>
      </main>
      <Footer />
    </>
  );
}

export default ErrorPage;