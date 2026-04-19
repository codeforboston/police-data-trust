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
  canEdit?: boolean
  editHref?: string
  showFollowerStats?: boolean
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
  isOwnProfile,
  canEdit,
  editHref,
  showFollowerStats = true
}: Props) {
  const router = useRouter()

  const [isFollowing, setIsFollowing] = useState(false)

  return (
    <Card
      variant="outlined"
      sx={{ marginTop: "24px", borderColor: "#CCCCCC", borderRadius: "10px" }}
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
          position: "relative"
        }}
      >
        {canEdit ? (
          <Button
            className={styles.editButton}
            variant="text"
            size="small"
            startIcon={<ModeEditOutlinedIcon />}
            onClick={() => router.push(editHref || "/profile/edit")}
          >
            Edit organization profile
          </Button>
        ) : null}
        {isOwnProfile ? (
          <IconButton className={styles.editIcon} sx={{ color: "#000" }}>
            <ModeEditOutlinedIcon onClick={() => router.push(editHref || "/profile/edit")} />
          </IconButton>
        ) : null}
        <div className={styles.container}>
          <Avatar sx={{ width: 160, height: 160 }} src={avatarUrl || "/broken-image.jpg"} />
          <div className={styles.info}>
            <Typography className={styles.name} component="h1">
              {firstName} {lastName}
            </Typography>
            <div className={styles.meta}>
              {title && <Typography className={styles.metaText}>{title}</Typography>}
              {organization && <Typography className={styles.metaText}>{organization}</Typography>}
              {(city || state) && (
                <Typography className={styles.metaText}>
                  {[city, state].filter(Boolean).join(", ")}
                </Typography>
              )}
            </div>
          </div>
        </div>

        <div className={styles.bio}>
          <p className={styles.bioText}>{biography}</p>
          {!isOwnProfile && !canEdit && (
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
          {showFollowerStats ? (
            <div className={styles.followerStats}>50 followers • 30 following</div>
          ) : null}
        </div>
      </CardContent>
    </Card>
  )
}
