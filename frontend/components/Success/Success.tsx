import Box from "@mui/material/Box";
import Image from "next/image";
import Link from "@mui/material/Link";
import logo from "@/public/images/NPDC_Logo_FINAL blue2 1.svg";
import styles from "./success.module.css";

type SuccessProps = {
  copy: string
}

const Success = ({ copy }: SuccessProps ) => {
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
          { copy }
        </p>
        <Link href="/" className={styles.link}>
          Return Home
        </Link>
      </Box>
    </div>
  )
}

export default Success;