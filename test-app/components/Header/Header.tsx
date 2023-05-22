import React from "react";
import Link from "next/link";
import s from "./Header.module.scss";
import Logo from "../Logo/Logo";

const Header: React.FC = () => {
  return (
    <header className={s.header}>
      <div className={s.logo}>
        <Link href="/">
          <a>
            <Logo />
          </a>
        </Link>
      </div>
      <nav className={s.nav}>
        <ul>
          <li>
            <Link href="/">
              <a>Home</a>
            </Link>
          </li>
          <li>
            <Link href="/about">
              <a>About</a>
            </Link>
          </li>
          <li>
            <Link href="/contact">
              <a>Contact</a>
            </Link>
          </li>
          <li>
            <Link href="/login">
              <a>Login</a>
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
``