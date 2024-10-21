import { Outlet } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import { Header, Footer } from "../components";

import "react-toastify/dist/ReactToastify.css";

const Root = () => {
  return (
    <div className="h-100 d-flex flex-column">
      <div className="fixed-top">
        <Header />
      </div>
      <div className="flex-grow-1 bg-body-tertiary" style={{ marginTop: 72 }}>
        <Outlet />
        <ToastContainer />
      </div>
      <Footer />
    </div>
  );
};

export { Root };
