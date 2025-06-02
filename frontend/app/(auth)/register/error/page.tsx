import React from "react";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Image from "next/image";
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg";
import styles from "./registrationError.module.css";

export default async function RegistrationError() {
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
                <h1 className={styles.h1}>Success!</h1>
                <p className={styles.p}>
                    We weren’t able to complete your registration.
                    Please come back and try again later.
                    If the problem persists, <a>please alert our development team</a>
                </p>
                <Link href="/" className={styles.link}>
                Return Home
                </Link>
            </Box>
        </div>
    );
}