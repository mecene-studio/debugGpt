import React from "react";
import s from "./Header.module.scss";

const Header: React.FC = () => {
  return (
    <div className={s.container}>
      <div className={s.title}>Header</div>
    </div>
  );
};

export default Header;
