import * as React from 'react'
import { ProfileMenu } from '../../models/profile' 
import styles from './profile.module.css'


interface ProfileNavProps {
  currentItem: ProfileMenu,
  selectNav: Function
}

const menuItems = [
  { item: ProfileMenu.USER_INFO, text: "User Information" },
  { item: ProfileMenu.PROFILE_TYPE, text: "Profile Type" },
  { item: ProfileMenu.SAVED_RESULTS, text: "Saved Results" },
  { item: ProfileMenu.SAVED_SEARCHES, text: "Saved Searches" }
]


export default function ProfileNav({ currentItem, selectNav }: ProfileNavProps) {

  const clsName = (itm: string) => itm === currentItem ? 'selected' : ''

  return (
    <nav className={styles.leftMenu}>
      <ul>
        {menuItems.map(itm => (
          <li key={itm.item} onClick={() => selectNav(itm.item)} className={clsName(itm.item)}>
            {itm.text}
          </li>
        ))}
      </ul>
    </nav>
  )
}