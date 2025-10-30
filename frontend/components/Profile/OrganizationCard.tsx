import React from "react"
import { Avatar, Card, CardContent, Typography } from "@mui/material"
import styles from "./organizationCard.module.css"

export default function OrganizationCard() {
  return (
    <Card variant="outlined" sx={{ marginTop: "20px" }}>
      <CardContent
        sx={{
          p: "40px",
          "&:last-child": {
            pb: "40px"
          },
          "@media (max-width:430px)": {
            p: "24px",
            "&:last-child": {
              pb: "24px"
            }
          }
        }}
      >
        <Typography variant="h5" fontWeight={600}>
          Organization Affiliation
        </Typography>
        <div className={styles.container}>
          <Avatar sx={{ width: 40, height: 40 }} src={"/broken-image.jpg"} />
          <div className={styles.containerText}>
            <Typography fontWeight={500} fontSize={20}>
              Organization Name
            </Typography>
            <Typography>Bio from the organization’s profile.</Typography>
          </div>
        </div>
        <Typography color="text.secondary">Joined on Oct 18, 2024</Typography>
        <div className={styles.container}>
          <Avatar sx={{ width: 40, height: 40 }} src={"/broken-image.jpg"} />
          <div className={styles.containerText}>
            <Typography fontWeight={500} fontSize={20}>
              Organization Name
            </Typography>
            <Typography>Bio from the organization’s profile.</Typography>
          </div>
        </div>
        <Typography color="text.secondary">Joined on Oct 18, 2024</Typography>
      </CardContent>
    </Card>
  )
}
