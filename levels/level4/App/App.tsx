import React from "react";
import s from "./App.module.scss";

const App: React.FC = () => {
  return (
    <div className={s.container}>
      <HeaderComponent />
      <BodyComponent />
      <FooterComponent text="Footer Text" />
    </div>
  );
};

export default App;
