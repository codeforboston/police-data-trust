'use client'

import Image from "next/image"
import { usePathname } from "next/navigation"




export default function NavLinks({props}) {

    const pathname = usePathname();

  return (
    <div>
        <ul>
            {props.map((prop) => (
                const isActive = pathname === prop.href;
                return(
                    <li key={`${props.text}`} className={ isAcitve? 'styles.activeLink' : 'styles.inactiveLink'} ></li>
                )
        </ul>
    </div>

  )}
