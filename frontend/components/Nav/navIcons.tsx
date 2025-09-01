"use client"

import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline"
import ChatBubbleOutlineOutlinedIcon from "@mui/icons-material/ChatBubbleOutlineOutlined"
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined"
import PersonOutlineOutlinedIcon from "@mui/icons-material/PersonOutlineOutlined"
import Link from "next/link"
import styles from "./navIcons.module.css"
import { useAuthState } from "@/utils/useAuthState"

export default function NavIcons() {
  const { isLoggedIn } = useAuthState()
  return (
    <div className={styles.icons}>
      {!isLoggedIn && (
        <Link href="/register" className={styles.createIcon}>
          <AddCircleOutlineIcon />
        </Link>
      )}
      <Link href="/chat" className={styles.iconLink}>
        <ChatBubbleOutlineOutlinedIcon />
      </Link>
      <Link href="/notify" className={styles.iconLink}>
        <NotificationsOutlinedIcon />
      </Link>
      <Link href="/profile" className={styles.iconLink}>
        <PersonOutlineOutlinedIcon />
      </Link>
    </div>
  )
}
