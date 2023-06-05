import React from "react";
import HeaderComponent from "../Header/Header";
import BodyComponent from "../Body/Body";
import FooterComponent from "../Footer/Footer";
import s from "./App.module.scss";

const App: React.FC = () => {
  return (
    <div className={s.container}>
      <HeaderComponent />
      <BodyComponent />
      <FooterComponent text={"Footer"} />
    </div>
  );
};

export default App;
