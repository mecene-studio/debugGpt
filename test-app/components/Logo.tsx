import React from "react";
import s from "./Logo.module.scss";

const Logo: React.FC = () => {
  return (
    <div className={s.container}>
      <div className={s.logo} />
      <BrainCircuit />
    </div>
  );
};

export default Logo;
