import { Outlet } from "react-router-dom";

import { Header, Footer } from "@components";

import "./root.css";

const Root = () => {
  return (
    <div className="root d-flex flex-column bg-body-tertiary">
      <Header />
      <Outlet />
      <div className="mt-auto">
        <Footer />
      </div>
    </div>
  );
};

export { Root };
