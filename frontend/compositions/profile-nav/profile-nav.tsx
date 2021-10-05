import * as React from "react"
import { ProfileMenu } from "../../models/profile"
import styles from "./profile-nav.module.css"

interface ProfileNavProps {
  currentItem: ProfileMenu
  selectNav: Function
}

const menuItems = [
  { item: ProfileMenu.USER_INFO, text: "User Information" },
  { item: ProfileMenu.PROFILE_TYPE, text: "Profile Type" },
  { item: ProfileMenu.SAVED_RESULTS, text: "Saved Results" },
  { item: ProfileMenu.SAVED_SEARCHES, text: "Saved Searches" }
]

export default function ProfileNav({ currentItem, selectNav }: ProfileNavProps) {
  const clsName = (itm: string) => (itm === currentItem ? styles.selectedItem : styles.menuItem)

  return (
    <nav className={styles.leftMenu}>
      <ul>
        {menuItems.map((mnu) => (
          <li key={mnu.item} onClick={() => selectNav(mnu.item)} className={clsName(mnu.item)}>
            {mnu.text}
          </li>
        ))}
      </ul>
    </nav>
  )
}
