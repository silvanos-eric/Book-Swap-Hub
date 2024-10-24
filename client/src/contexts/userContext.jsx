import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";

import { useCheckSession } from "../hooks";

// Create the UserContext
const UserContext = createContext();

const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const { checkUserSession } = useCheckSession();

  // Check session on app load or refresh
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await checkUserSession(); // Ensure asynchronous call is awaited
        setUser(user);
      } catch (error) {
        error;
      }
    };

    fetchUser();
  }, [navigate, checkUserSession]); // Make sure useEffect has proper dependencies

  // Redirect based on user state changes
  const login = (data) => {
    setUser(data);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
};

UserProvider.propTypes = {
  children: PropTypes.node,
};

export { UserContext, UserProvider };
