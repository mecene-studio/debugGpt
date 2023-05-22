import React from "react";
import s from "./Logo.module.scss";
import { Icon } from "@lucide/react";

const Logo: React.FC = () => {
  return (
    <div className={s.logo}>
      <Icon name="code" size={32} />
      <h1>My App</h1>
    </div>
  );
};

export default Logo;