import { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";

import { Container, Navbar, Nav } from ".";
import { useLogout } from "../hooks";
import { UserContext } from "../contexts";

const Header = () => {
  const navigate = useNavigate();
  const { logOutUser } = useLogout();
  const { user } = useContext(UserContext);

  const handleLogout = () => {
    navigate("/", { replace: true });
    logOutUser();
    navigate("/");
  };

  const userHomeLink = user?.roleNameList.includes("customer")
    ? "/customer-home"
    : "/vendor-home";

  return (
    <Navbar expand="lg" className="bg-white p-3">
      <Container>
        <Navbar.Brand as={NavLink} to="/">
          Book Swap Hub
        </Navbar.Brand>
        {user && (
          <Nav>
            <Nav.Link as={NavLink} to={userHomeLink}>
              Home
            </Nav.Link>
          </Nav>
        )}
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            {!user && (
              <>
                <Nav.Link as={NavLink} to="/login">
                  Log In
                </Nav.Link>
                <Nav.Link as={NavLink} to="/signup">
                  Sign up
                </Nav.Link>
              </>
            )}
            <Nav.Link as={NavLink} to="/books">
              Catalogue
            </Nav.Link>
            {!!user && (
              <Nav.Link as="button" onClick={handleLogout}>
                Logout
              </Nav.Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export { Header };
