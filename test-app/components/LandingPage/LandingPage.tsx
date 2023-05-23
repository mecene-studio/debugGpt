import React from "react";
import AppLayout from "../AppLayout";
import Button from "../Button";
export default function LandingPage() {
  return (
    <AppLayout>
      <div className={s.container}>
        <Logo />
        <Button />
      </div>
    </AppLayout>
  );
}
