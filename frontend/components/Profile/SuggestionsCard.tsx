import React, { useState } from "react"
import Avatar from "@mui/material/Avatar"
import Button from "@mui/material/Button"
import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import Typography from "@mui/material/Typography"
import styles from "./suggestionsCard.module.css"

interface Suggestion {
  name: string
  title: string
  avatarUrl?: string
}

interface SuggestionsCardProps {
  title: string
  items: Suggestion[]
  onFollow?: (name: string) => void
  onUnfollow?: (name: string) => void
}

export default function SuggestionsCard({
  title,
  items,
  onFollow,
  onUnfollow
}: SuggestionsCardProps) {
  const [followedUsers, setFollowedUsers] = useState<Set<string>>(new Set())

  const toggleFollow = (name: string) => {
    setFollowedUsers((prev) => {
      const newSet = new Set(prev)
      if (newSet.has(name)) {
        newSet.delete(name)
        onUnfollow?.(name)
      } else {
        newSet.add(name)
        onFollow?.(name)
      }
      return newSet
    })
  }

  return (
    <Card variant="outlined">
      <CardContent
        sx={{
          display: "flex",
          flexDirection: "column",
          padding: "24px",
          gap: "24px",
          width: "266px"
        }}>
        <Typography variant="h6" component="p" fontWeight={600} fontStyle={"semi-bold"}>
          {title}
        </Typography>
        {items.map((item, index) => {
          const isFollowing = followedUsers.has(item.name)
          return (
            <div key={index} className={styles.suggestionItem}>
              <Avatar src={item.avatarUrl || "/broken-image.jpg"} />
              <div className={styles.textContainer}>
                <p className={styles.name}>{item.name}</p>
                <p>{item.title}</p>
                <Button
                  color="primary"
                  size="small"
                  variant={isFollowing ? "text" : "outlined"}
                  onClick={() => toggleFollow(item.name)}
                  sx={{ width: "fit-content", marginTop: "8px" }}>
                  {isFollowing ? "Following" : "Follow"}
                </Button>
              </div>
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
