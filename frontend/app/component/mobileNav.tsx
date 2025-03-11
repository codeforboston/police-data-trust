'use client'

import Link from "next/link";
import styles from "./mobileNav.module.css";
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import TimelineOutlinedIcon from '@mui/icons-material/TimelineOutlined';
import ControlPointOutlinedIcon from '@mui/icons-material/ControlPointOutlined';
import PeopleOutlinedIcon from '@mui/icons-material/PeopleOutlined';
import HistoryOutlinedIcon from '@mui/icons-material/HistoryOutlined';

export default function MobileNav() {

      return (
        <div className={styles.mobileNav}>
            <ul className={styles.ul}>
                <li className={styles.li}>
                    <HomeOutlinedIcon className={styles.icon} />
                    <Link href="/">Home</Link>
                </li>
                <li className={styles.li}>
                    <TimelineOutlinedIcon className={styles.icon} />  
                    <Link href="/2">Data Explore</Link>
                </li>
                <li className={styles.li}>
                    <div className= {styles.create}>
                        <ControlPointOutlinedIcon className={styles.icon} /> 
                        <Link href="/3">Create</Link>
                    </div> 
                </li>
                <li className={ styles.li}>
                    <PeopleOutlinedIcon className={styles.icon} />    
                    <Link href="/4">Community</Link>
                </li>
                <li className={styles.li}> 
                    <HistoryOutlinedIcon className={styles.icon} />  
                    <Link href="/5">Collection</Link>
                </li>
            </ul>
        </div>
      )
}