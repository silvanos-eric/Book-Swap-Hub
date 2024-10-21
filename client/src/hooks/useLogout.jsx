import { useContext, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

import { logout as logoutApi } from "../api";
import { UserContext } from "../contexts";

const useLogout = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { logout } = useContext(UserContext);

  const logOutUser = useCallback(async () => {
    try {
      setLoading(true);
      logoutApi();
      logout();
      navigate("/");
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error(error);
    }
  }, [logout, navigate]);

  return {
    logOutUser,
    loading,
  };
};

export { useLogout };
