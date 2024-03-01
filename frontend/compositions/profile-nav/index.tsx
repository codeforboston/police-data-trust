import * as React from "react"
import { ProfileMenu, profileMenuItems } from "../../models/profile"
import styles from "./profile-nav.module.css"

interface ProfileNavProps {
  activePage: ProfileMenu
  setActivePage: React.Dispatch<React.SetStateAction<ProfileMenu>>
}

export default function ProfileNav({ activePage, setActivePage }: ProfileNavProps) {
  const clsName = (item: string) => (item === activePage ? styles.selectedItem : styles.menuItem)

  return (
    <nav className={styles.leftMenu}>
      <ul>
        {profileMenuItems.map((menu) => (
          <li
            key={menu.item}
            onClick={() => setActivePage(menu.item)}
            className={clsName(menu.item)}>
            {menu.text}
          </li>
        ))}
      </ul>
    </nav>
  )
}
