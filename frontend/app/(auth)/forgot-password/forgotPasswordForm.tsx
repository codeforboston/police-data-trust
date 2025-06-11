"use client"

import Image from "next/image"
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"
import useResetPassword from "./useForgotPassword"
import Box from "@mui/material/Container"
import TextField from "@mui/material/TextField"
import Button from "@mui/material/Button"
import Link from "@mui/material/Link"

import styles from "./resetPasswordForm.module.css"

type FormErrorMessages = {
  email: string
}

const formErrorMessages: FormErrorMessages = {
  email: "Invalid Email"
}

const ForgotPasswordForm = () => {
  const { handleSubmit, handleChange, formError, email } = useResetPassword()

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
        <h1 className={styles.h1}>Forgot Your Password?</h1>
        <form className={styles.form} noValidate autoComplete="on" onSubmit={handleSubmit}>
          <p className={styles.p}>
            Please enter the email address you used to register for your account.
          </p>
          <TextField
            required
            id="email"
            autoComplete="email"
            value={email}
            label="Email"
            variant="outlined"
            sx={{ width: "100%", py: "5px" }}
            margin="dense"
            onChange={handleChange}
            error={formError ? true : false}
            helperText={formErrorMessages.email}
          />
          <Button type="submit" variant="contained" color="primary" sx={{ mt: 2, width: "100%" }}>
            Send Password Reset
          </Button>
        </form>
        <p className={`${styles["p--bold"]} ${styles.p}`}>
          Or do you remember your login credentials?
        </p>
        <Link href="/login" className={styles.link}>
          Return to Login
        </Link>
      </Box>
    </div>
  )
}

export default ForgotPasswordForm
