"use client"

import Image from "next/image"
import Box from "@mui/material/Box"
import Link from "@mui/material/Link"
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"
import styles from "./logout.module.css"
import { useAuth } from "@/context/AuthProvider"
import { useEffect } from "react"

const Logout = () => {
  const { removeAuthToken } = useAuth()
  useEffect(() => {
    removeAuthToken()
  }, [removeAuthToken])

  return (
    <div>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "84vh",
          flexDirection: "column"
        }}
      >
        <Image src={logo} alt="NPDC Logo" width={100} height={100} />
        <h1 className={styles.h1}>You got logged out!</h1>
        <Link href="/" className={styles.link}>
          Return Home
        </Link>
      </Box>
    </div>
  )
}

export default Logout
