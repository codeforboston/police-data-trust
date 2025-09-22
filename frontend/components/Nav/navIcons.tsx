"use client"

import React from "react"
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline"
import ChatBubbleOutlineOutlinedIcon from "@mui/icons-material/ChatBubbleOutlineOutlined"
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined"
import PersonOutlineOutlinedIcon from "@mui/icons-material/PersonOutlineOutlined"
import Link from "next/link"
import { useRouter } from "next/navigation"
import styles from "./navIcons.module.css"
import { useAuthState } from "@/utils/useAuthState"
import { Button, ClickAwayListener, Grow, MenuItem, MenuList, Paper, Popper } from "@mui/material"

export default function NavIcons() {
  const { isLoggedIn } = useAuthState()
  const router = useRouter()

  const [open, setOpen] = React.useState(false)
  const anchorRef = React.useRef<HTMLButtonElement>(null)

  const handleToggle = () => {
    setOpen((prevOpen) => !prevOpen)
  }

  const handleClose = (event: Event | React.SyntheticEvent) => {
    if (anchorRef.current && anchorRef.current.contains(event.target as HTMLElement)) {
      return
    }

    setOpen(false)
  }

  function handleListKeyDown(event: React.KeyboardEvent) {
    if (event.key === "Tab") {
      event.preventDefault()
      setOpen(false)
    } else if (event.key === "Escape") {
      setOpen(false)
    }
  }

  function handleProfile() {
    setOpen(false)
    window.location.href = "/profile"
  }

  function handleLogout() {
    setOpen(false)
    router.push("/logout")
  }

  // return focus to the button when we transitioned from !open -> open
  const prevOpen = React.useRef(open)
  React.useEffect(() => {
    if (prevOpen.current === true && open === false) {
      anchorRef.current!.focus()
    }

    prevOpen.current = open
  }, [open])

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
      {!isLoggedIn ? (
        <Button
          variant="outlined"
          href="/login"
          sx={{
            color: "#303463",
            borderColor: "#303463",
            ":hover": { backgroundColor: "#ECEEF8" }
          }}>
          Sign In
        </Button>
      ) : (
        <>
          <Button
            ref={anchorRef}
            sx={{
              color: "#303463",
              borderColor: "#303463",
              backgroundColor: "transparent",
              "&:hover": {
                backgroundColor: "#ECEEF8"
              },
              minWidth: "40px",
              paddingBlock: "8px"
            }}
            id="profile-button"
            aria-controls={open ? "profile-menu" : undefined}
            aria-expanded={open ? "true" : undefined}
            aria-haspopup="true"
            onClick={handleToggle}>
            <PersonOutlineOutlinedIcon />
          </Button>
          <Popper
            open={open}
            anchorEl={anchorRef.current}
            role={undefined}
            placement="bottom-start"
            transition
            disablePortal>
            {({ TransitionProps, placement }) => (
              <Grow
                {...TransitionProps}
                style={{
                  transformOrigin: placement === "bottom-start" ? "left top" : "left bottom"
                }}>
                <Paper>
                  <ClickAwayListener onClickAway={handleClose}>
                    <MenuList
                      autoFocusItem={open}
                      id="profile-menu"
                      aria-labelledby="profile-button"
                      onKeyDown={handleListKeyDown}>
                      <MenuItem
                        onClick={handleProfile}
                        sx={{ "&:hover": { backgroundColor: "#ECEEF8" } }}>
                        Profile
                      </MenuItem>
                      <MenuItem
                        onClick={handleLogout}
                        sx={{ "&:hover": { backgroundColor: "#ECEEF8" } }}>
                        Logout
                      </MenuItem>
                    </MenuList>
                  </ClickAwayListener>
                </Paper>
              </Grow>
            )}
          </Popper>
        </>
      )}
    </div>
  )
}
