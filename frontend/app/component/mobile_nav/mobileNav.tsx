'use client'

import Link from "next/link";
import styles from "./mobileNav.module.css";
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import TimelineOutlinedIcon from '@mui/icons-material/TimelineOutlined';
import ControlPointOutlinedIcon from '@mui/icons-material/ControlPointOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import HistoryOutlinedIcon from '@mui/icons-material/HistoryOutlined';
import { usePathname } from "next/navigation";


export default function MobileNav() {

    const pathname = usePathname();

      return (
        <div className={styles.mobileNav}>
            <ul className={styles.ul}>
                <li className={ pathname === "/" ? `${styles.active}`: styles.li}>
                    <HomeOutlinedIcon className={styles.icon} />
                    <Link href="/">Home</Link>
                </li>
                <li className={ pathname === "/2" ? `${styles.active}`: styles.li}>
                    <TimelineOutlinedIcon className={styles.icon} />  
                    <Link href="/2">Data Explore</Link>
                </li>
                <li className={ pathname === "/3" ? `${styles.active}`: styles.li}>
                    <div className= {styles.create}>
                        <ControlPointOutlinedIcon className={styles.icon} /> 
                        <Link href="/3">Create</Link> 
                    </div> 
                </li>
                <li className={ pathname === "/4" ? `${styles.active}`: styles.li}>
                    <PeopleOutlinedIcon className={styles.icon} />    
                    <Link href="/4">Community</Link>
                </li>
                <li className={ pathname === "/5" ? `${styles.active}`: styles.li}> 
                    <HistoryOutlinedIcon className={styles.icon} />  
                    <Link href="/5">Collection</Link>
                </li>
            </ul>
        </div>
      )
}