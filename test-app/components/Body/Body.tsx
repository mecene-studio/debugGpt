import React from "react";
import s from "./Body.module.scss";
import Confetti from "react-confetti";

export default function BodyComponent() {
  const screenDimensions = [1920, 1080];
  return (
    <div className={s.container}>
      <Confetti width={screenDimensions[0]} height={screenDimensions[1]} />
      <div className={s.title}>LEVEL 4</div>
    </div>
  );
}
