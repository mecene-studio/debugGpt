import React from "react";
import s from "./App.module.scss";

const App: React.FC = () => {
  return (
    <div className={s.container}>
      <Header />
      <Body />
      <Footer />
    </div>
  );
};

export default App;
