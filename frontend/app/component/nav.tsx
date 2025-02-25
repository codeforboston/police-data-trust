'use server'

import Image from "next/image";
import Link from "next/link";
import Logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"

export default async function Nav() {
  return (
    <nav>
      <div>
        <Image src={Logo} alt="Logo" width={70} height={70} />
      <div>
        <p>National Police Data</p>
        <p>The national index of police incidents </p>
      </div>
      </div>
    </nav>
  );
}