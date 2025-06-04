"use client";
import styles from "./page.module.css";
import { isLoggedIn } from "../utils/auth";

export default function Home() {
  const [storedValue, setValue] = isLoggedIn();
  return (
    <div className={styles.page}>
      <h1>This is the Home Page!</h1>
      <p className={styles.txt}> More to come soon!</p>
      <p className={styles.txt}>
        {storedValue ? "You are logged in!" : "You are not logged in."}
      </p>
    </div>
  );
}
