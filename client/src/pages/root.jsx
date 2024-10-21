import { Outlet } from "react-router-dom";

import { Header, Footer } from "../components";

const Root = () => {
  return (
    <div className="h-100 d-flex flex-column">
      <div className="fixed-top">
        <Header />
      </div>
      <div className="flex-grow-1 bg-body-tertiary" style={{ marginTop: 72 }}>
        <Outlet />
      </div>
      <Footer />
    </div>
  );
};

export { Root };
