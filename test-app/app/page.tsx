"use client";

import styles from "./page.module.scss";
import LandingPage from "@/components/LandingPage";

export default function Home() {
  return (
    <main className={styles.main}>
      <LandingPage />
    </main>
  );
}
