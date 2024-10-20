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
    const checkSession = async () => {
      try {
        const user = await checkUserSession(); // Ensure asynchronous call is awaited
        setUser(user);
        console.log(user);
        if (user.role_name_list.includes("customer")) {
          navigate("/customer-home");
        } else if (user.role_name_list.includes("vendor")) {
          navigate("/vendor-home");
        } else {
          setUser(null);
          navigate("/", { replace: true });
        }
      } catch (error) {
        console.error(error);
      }
    };

    checkSession();
  }, [navigate, checkUserSession]); // Make sure useEffect has proper dependencies

  // Redirect based on user state changes
  useEffect(() => {
    if (user == null) {
      navigate("/", { replace: true });
    } else if (user.role_name_list.includes("customer")) {
      navigate("/customer-home");
    } else if (user.role_name_list.includes("vendor")) {
      // Fix typo here
      navigate("/vendor-home");
    }
  }, [user, navigate]);

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
