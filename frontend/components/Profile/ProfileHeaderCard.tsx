"use client"

import styles from "./profileHeaderCard.module.css"
import { Avatar, Button, Card, CardContent, Typography, IconButton } from "@mui/material"
import ModeEditOutlinedIcon from "@mui/icons-material/ModeEditOutlined"
import { useRouter } from "next/navigation"
import { useState } from "react"

interface Props {
  firstName: string
  lastName: string
  avatarUrl?: string
  biography?: string
  title?: string
  organization?: string
  city?: string
  state?: string
  isOwnProfile?: boolean
}

export default function ProfileHeaderCard({
  firstName,
  lastName,
  avatarUrl,
  biography,
  title,
  organization,
  city,
  state,
  isOwnProfile
}: Props) {
  const router = useRouter()

  const [isFollowing, setIsFollowing] = useState(false)

  return (
    <Card variant="outlined" sx={{ marginTop: "24px" }}>
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
        {isOwnProfile && (
          <IconButton className={styles.editIcon} sx={{ color: "#000" }}>
            <ModeEditOutlinedIcon onClick={() => router.push("/profile/edit")} />
          </IconButton>
        )}
        <div className={styles.container}>
          <Avatar sx={{ width: 160, height: 160 }} src={avatarUrl || "/broken-image.jpg"} />
          <div className={styles.info}>
            <Typography variant="h5" fontWeight={600} lineHeight={1}>
              {firstName} {lastName}
            </Typography>
            <div className={styles.meta}>
              {title && <Typography lineHeight={1}>{title}</Typography>}
              {organization && <Typography lineHeight={1}>{organization}</Typography>}
              {(city || state) && (
                <Typography lineHeight={1}>{[city, state].filter(Boolean).join(", ")}</Typography>
              )}
            </div>
          </div>
        </div>

        <div className={styles.bio}>
          <p>{biography}</p>
          {!isOwnProfile && (
            <div className={styles.actions}>
              <Button
                color="primary"
                variant={isFollowing ? "text" : "contained"}
                onClick={() => setIsFollowing(!isFollowing)}
              >
                {isFollowing ? "Following" : "Follow"}
              </Button>

              <Button color="primary" variant="outlined">
                Message
              </Button>
            </div>
          )}
          <div className={styles.followerStats}>50 followers • 30 following</div>
        </div>
      </CardContent>
    </Card>
  )
}
