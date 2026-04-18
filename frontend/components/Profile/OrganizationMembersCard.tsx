import React from "react"
import { Avatar, Button, Card, CardContent, Typography } from "@mui/material"
import styles from "./organizationMembersCard.module.css"
import { SourceMember } from "@/utils/api"

export default function OrganizationMembers({ members }: { members: SourceMember[] }) {
  if (!members.length) {
    return null
  }

  return (
    <Card
      variant="outlined"
      sx={{
        marginTop: "20px",
        marginBottom: "20px",
        borderColor: "#CCCCCC",
        borderRadius: "10px"
      }}
    >
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
          },
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "24px"
        }}
      >
        <Typography
          variant="h5"
          fontWeight={600}
          sx={{
            fontFamily: "Inter, Roboto, sans-serif",
            fontSize: "24px",
            lineHeight: "29px"
          }}
        >
          Organization Members
        </Typography>
        <div className={styles.membersGrid}>
          {members.map((item) => {
            return (
              <div key={item.uid} className={styles.memberItem}>
                <Avatar
                  src={item.profile_image || "/broken-image.jpg"}
                  sx={{ width: 60, height: 60 }}
                />

                <p className={styles.name}>{`${item.first_name} ${item.last_name}`}</p>
                {item.title ? <p>{item.title}</p> : null}
                {item.organization ? <p>{item.organization}</p> : null}
                <Button color="primary" size="small" variant="outlined" className={styles.viewButton}>
                  View Profile
                </Button>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
