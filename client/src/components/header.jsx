import { Link, useNavigate } from "react-router-dom";

import { Container, Navbar, Nav } from ".";

const Header = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/", { replace: true });
  };

  return (
    <Navbar expand="lg" className="bg-body-tertiary sticky-top">
      <Container>
        <Navbar.Brand as={Link} to="/">
          Book Swap Hub
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={Link} to="/login">
              Login
            </Nav.Link>
            <Nav.Link as={Link} to="/signup">
              Sign up
            </Nav.Link>
            <Nav.Link as={Link} to="/books">
              Books
            </Nav.Link>
            <Nav.Link as="button" onClick={handleLogin}>
              Logout
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export { Header };
