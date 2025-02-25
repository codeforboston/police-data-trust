'use server'
import Link from "next/link";
export default async function Nav() {
  return (
    <nav>
      <ul>
        <li>
          <Link href="/">Home</Link>
        </li>
        <li>
          <Link href="/about">Data explorer</Link>
        </li>
        <li>
            <Link href="/community">Community</Link>
        </li>
        <li>
            <Link href="/collection">Collection</Link>
        </li>
      </ul>
    </nav>
  );
}