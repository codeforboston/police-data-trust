"use client";

import React from "react";
import { useState } from "react";
import styles from "./register.module.css";
import Image from "next/image";
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg";
import Box from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import OutlinedInput from "@mui/material/OutlinedInput";
import FormControl from "@mui/material/FormControl";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import InputLabel from "@mui/material/InputLabel";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
// import createrUser from "@/lib/createUser";

export default function RegistrationForm() {
  const [showPassword, setShowPassword] = React.useState(false);

  type UserData = {
    email: string;
    firstname: string;
    lastname: string;
    phone: string;
    password: string;
    password2: string;
  };

  type FormErrorMessages = {
    email: string;
    name: string;
    password: string;
  };

  const formErrorMessages: FormErrorMessages = {
    email: "Invalid Email",
    name: "Required",
    password: "Invalid Password or Do Not Match",
  };

  const [userData, setUserData] = useState<UserData>({
    email: "",
    firstname: "",
    lastname: "",
    phone: "",
    password: "",
    password2: "",
  });

  const [formError, setFormError] = useState(false);

  const handleChange = (e) => {
    setUserData({ ...userData, [e.target.id]: e.target.value });
  };

  const handleFormError = (data: UserData) => {
    if (data.firstname == "" || data.lastname == "") {
      setFormError(true);
      return;
    }

    if (data.email == "" || !data.email.includes("@")) {
      setFormError(true);
      return;
    }

    if (data.password != data.password2) {
      setFormError(true);
      return;
    }
    if (data.phone === "") {
      setFormError(true);
      return;
    }
    if (data.password === "" || data.password2 === "") {
      setFormError(true);
    } else {
      setFormError(false);
      // console.log(createrUser(userData));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    handleFormError(userData);

    console.log(userData);
  };

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (
    event: React.MouseEvent<HTMLButtonElement>,
  ) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (
    event: React.MouseEvent<HTMLButtonElement>,
  ) => {
    event.preventDefault();
  };

  return (
    <div>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "84vh",
          flexDirection: "column",
        }}
      >
        <Image src={logo} alt="NPDC Logo" width={100} height={100} />
        <h1 className={styles.h1}>Create Account</h1>
        <form
          className={styles.form}
          noValidate
          autoComplete="on"
          onSubmit={handleSubmit}
        >
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
          <TextField
            required
            id="firstname"
            value={userData.firstname}
            label="First Name"
            variant="outlined"
            sx={{ width: "100%" }}
            margin="dense"
            onChange={handleChange}
            error={formError ? true : false}
            helperText={formErrorMessages.name}
          />
          <TextField
            required
            id="lastname"
            value={userData.lastname}
            label="Last Name"
            variant="outlined"
            sx={{ width: "100%" }}
            margin="dense"
            onChange={handleChange}
            error={formError ? true : false}
            helperText={formErrorMessages.name}
          />
          <TextField
            required
            id="phone"
            value={userData.phone}
            label="Phone Number"
            variant="outlined"
            sx={{ width: "100%" }}
            margin="dense"
            onChange={handleChange}
            error={formError ? true : false}
            helperText={formErrorMessages.name}
          />
          <p className={styles.p}>
            {" "}
            Passwords must be at least 8 characters long while containing one
            upper case letter, lower case letter, and symbol.
          </p>
          <FormControl
            sx={{ marginY: "5px", width: "100%" }}
            variant="outlined"
          >
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
                    aria-label={
                      showPassword
                        ? "hide the password"
                        : "display the password"
                    }
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
          <FormControl
            varient="outlined"
            sx={{ width: "100%", marginY: "5px" }}
          >
            <InputLabel htmlFor="password">Confirm Password</InputLabel>
            <OutlinedInput
              id="password2"
              value={userData.password2}
              autoComplete="new-password"
              type={showPassword ? "text" : "password"}
              onChange={handleChange}
              error={formError ? true : false}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label={
                      showPassword
                        ? "hide the password"
                        : "display the password"
                    }
                    onClick={handleClickShowPassword}
                    onMouseDown={handleMouseDownPassword}
                    onMouseUp={handleMouseUpPassword}
                    edge="end"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Confirm Password"
            />
          </FormControl>
          <Button
            variant="contained"
            type="submit"
            sx={{ width: "100%", marginY: "20px", height: "50px" }}
          >
            Create Account
          </Button>
        </form>
      </Box>
    </div>
  );
}
