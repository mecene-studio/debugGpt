import React from "react";
import Link from "next/link";
import s from "./Header.module.scss";
import Logo from "./Logo";

const Header: React.FC = () => {
  return (
    <header className={s.container}>
      <Link href="/">
        <a>
          <Logo />
        </a>
      </Link>
    </header>
  );
};

export default Header;
