import React from "react";
import s from "./AppLayout.module.scss";
import Footer from "./Footer";
import Header from "./Header";

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  return (
    <div className={s.container}>
      <Header />
      <main className={s.main}>{children}</main>
      <Footer />
    </div>
  );
};

export default AppLayout;
