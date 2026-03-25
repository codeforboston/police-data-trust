import React, { useState } from "react"
import { Avatar, Button, Card, CardContent, Typography } from "@mui/material"
import styles from "./organizationMembersCard.module.css"

// TODO: Replace with real data
const members = [
  {
    firstName: "Jonathan",
    lastName: "Watkins",
    avatarUrl: "/broken-image.jpg",
    title: "Title",
    company: "Company Name",
    id: 0
  },
  {
    firstName: "Jonathan",
    lastName: "Watkins",
    avatarUrl: "/broken-image.jpg",
    title: "Title",
    company: "Company Name",
    id: 1
  },
  {
    firstName: "Jonathan",
    lastName: "Watkins",
    avatarUrl: "/broken-image.jpg",
    title: "Title",
    company: "Company Name",
    id: 2
  },
  {
    firstName: "Jonathan",
    lastName: "Watkins",
    avatarUrl: "/broken-image.jpg",
    title: "Title",
    company: "Company Name",
    id: 3
  },
  {
    firstName: "Jonathan",
    lastName: "Watkins",
    avatarUrl: "/broken-image.jpg",
    title: "Title",
    company: "Company Name",
    id: 4
  },
  {
    firstName: "Jonathan",
    lastName: "Watkins",
    avatarUrl: "/broken-image.jpg",
    title: "Title",
    company: "Company Name",
    id: 5
  }
]

export default function OrganizationMembers() {
  const [isFollowing, setIsFollowing] = useState(false)
  return (
    <Card variant="outlined" sx={{ marginTop: "20px", marginBottom: "20px" }}>
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
          alignItems: "center"
        }}
      >
        <Typography variant="h5" fontWeight={600}>
          Organization Members
        </Typography>
        <div className={styles.membersGrid}>
          {members.map((item) => {
            return (
              <div key={item.id} className={styles.memberItem}>
                <Avatar
                  src={item.avatarUrl || "/broken-image.jpg"}
                  sx={{ width: 60, height: 60 }}
                />

                <p className={styles.name}>{item.firstName}</p>
                <p className={styles.name}>{item.lastName}</p>
                <p>{item.title}</p>
                <p>{item.company}</p>
                <Button
                  color="primary"
                  size="small"
                  variant="outlined"
                  onClick={() => setIsFollowing(!isFollowing)}
                  sx={{ width: "fit-content", marginTop: "8px" }}
                >
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
