"use client"

import React from "react"
import styles from "./login.module.css"
import Image from "next/image"
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg"
import Box from "@mui/material/Container"
import TextField from "@mui/material/TextField"
import InputAdornment from "@mui/material/InputAdornment"
import OutlinedInput from "@mui/material/OutlinedInput"
import FormControl from "@mui/material/FormControl"
import Visibility from "@mui/icons-material/Visibility"
import VisibilityOff from "@mui/icons-material/VisibilityOff"
import InputLabel from "@mui/material/InputLabel"
import IconButton from "@mui/material/IconButton"
import Button from "@mui/material/Button"
import Link from "@mui/material/Link"
import Alert from "@mui/material/Alert"
import useLogin from "./useLogin"

type FormErrorMessages = {
  email: string
  name: string
  password: string
}

const formErrorMessages: FormErrorMessages = {
  email: "Invalid Email",
  name: "Required",
  password: "Invalid Password or Do Not Match"
}

export default function LoginForm() {
  const {
    handleSubmit,
    handleChange,
    userData,
    formError,
    showPassword,
    handleClickShowPassword,
    handleMouseDownPassword,
    handleMouseUpPassword
  } = useLogin()

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
        <h1 className={styles.h1}>Login</h1>
        <form className={styles.form} noValidate autoComplete="on" onSubmit={handleSubmit}>
          {formError && (
            <Alert
              severity="error"
              className="alert"
              sx={{ maxWidth: "350px", margin: "0 auto 10px auto" }}
            >
              The email or password you entered doesn’t match our records. Please try again.
            </Alert>
          )}
          <TextField
            required
            id="email"
            autoComplete="email"
            value={userData.email}
            label="Email"
            variant="outlined"
            sx={{ width: "100%", py: "5px" }}
            margin="dense"
            onChange={handleChange}
            error={formError ? true : false}
            helperText={formErrorMessages.email}
          />
          <FormControl sx={{ marginY: "5px", width: "100%" }} variant="outlined">
            <InputLabel htmlFor="password">Password</InputLabel>
            <OutlinedInput
              id="password"
              autoComplete="new-password"
              value={userData.password}
              type={showPassword ? "text" : "password"}
              onChange={handleChange}
              error={formError ? true : false}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label={showPassword ? "hide the password" : "display the password"}
                    onClick={handleClickShowPassword}
                    onMouseDown={handleMouseDownPassword}
                    onMouseUp={handleMouseUpPassword}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Password"
            />
          </FormControl>
          <Button
            variant="contained"
            type="submit"
            sx={{ width: "100%", marginY: "20px", height: "50px" }}
          >
            Login
          </Button>
          <Link href="/forgot-password">Forgot password?</Link>
          <p className={`${styles["p--bold"]} ${styles.p}`}>
            New to the National Police Data Coalition?{" "}
          </p>
          <Link className={styles.link} href="/register">
            Create an account
          </Link>
        </form>
      </Box>
    </div>
  )
}
