import styles from "./register.module.css";
import Image from "next/image";
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg";
import Box from "@mui/material/Container";
import  TextField  from "@mui/material/TextField";




export default async function Register() {
    return (
        <div>
            <RegistrationForm />
        </div>
    );
}

//Form for registration Client Component

export function RegistrationForm(){

    return (
        <div>
            <Box sx={{display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '84vh', flexDirection: 'column'}}>
                <Image src={logo} alt="NPDC Logo" width={100} height={100} />
                <h1 className={styles.h1}>Create Account</h1>
                <form className={styles.form} noValidate autoComplete="off">
                    <TextField required id="email" label="Email" variant="outlined" sx={{width: '100%', py: "5px"}} />
                    <TextField required id="first-name" label="First Name" variant="outlined" sx={{width: '100%', py: "10px"}}  />
                    <TextField required id="last-name" label="Last Name" variant="outlined" sx={{width: '100%', py: "10px"}}  />
                    <p className={styles.p}> Passwords must be at least 8 characters long while containing one upper case letter, lower case letter, and symbol.</p>
                    <TextField required id="password" label="Password" variant="outlined" type="password" sx={{width: '100%', py: "10px"}}  />
                    <TextField required id="confirm-password" label="Confirm Password" variant="outlined" type="password" sx={{width: '100%', py: "10px"}} />
                </form>
            </Box>
        </div>
    )
}