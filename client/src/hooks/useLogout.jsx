import { useContext, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

import { logout as logoutApi } from "../api";
import { UserContext } from "../contexts";
import { showInfoToast } from "../utils";

const useLogout = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { logout } = useContext(UserContext);

  const logOutUser = useCallback(async () => {
    setLoading(true);

    try {
      logoutApi(); // Clear session
      logout(); // Clear state
      navigate("/");
      showInfoToast("Logout success");
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
