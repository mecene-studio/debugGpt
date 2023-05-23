import React from "react";
import Header from "./Header/Header";
import { Footer } from "./Footer/Footer";
import s from "./AppLayout.module.scss";

const AppLayout: React.FC = ({ children }) => {
  return (
    <div className={s.container}>
      <Header />
      <main className={s.main}>{children}</main>
      <Footer />
    </div>
  );
};

export default AppLayout;
