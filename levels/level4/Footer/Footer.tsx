import React from "react";
import s from "./Footer.module.scss";

export default function FooterComponent(props: { text: string }) {
  return (
    <div className={s.container}>
      <div className={s.title}>{props.text}</div>
    </div>
  );
}
