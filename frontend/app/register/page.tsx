import React from "react";
import styles from "./register.module.css";
import  RegistrationForm  from "./registrationForm";
import Image from "next/image";
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg";
import Box from "@mui/material/Container";
import  TextField  from "@mui/material/TextField";
import  InputAdornment  from "@mui/material/InputAdornment";
import OutlinedInput  from "@mui/material/OutlinedInput";
import  FormControl  from "@mui/material/FormControl";
import Visibility  from "@mui/icons-material/Visibility";
import  VisibilityOff from "@mui/icons-material/VisibilityOff";
import { useState } from "react";





export default async function Register() {
    return (
        <div>
            <RegistrationForm />
        </div>
    );
}

//Form for registration Client Component

