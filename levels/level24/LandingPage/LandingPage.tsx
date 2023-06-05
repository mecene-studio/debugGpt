import React from "react";
import AppLayout from "../AppLayout";
import Button from "../Button";
import Logo from "../Logo";
import s from "./LandingPage.module.scss";

const LandingPage = () => {
  return (
    <AppLayout>
      <div className={s.container}>
        <Logo />
        <Button onClick={() => {}} text="Click me!" />
        <h1>Welcome to my Next.js app!</h1>
      </div>
    </AppLayout>
  );
};

export default LandingPage;
