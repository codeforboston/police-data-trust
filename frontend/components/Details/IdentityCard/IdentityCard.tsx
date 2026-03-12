import { Avatar, IconButton, Typography } from "@mui/material"
import type { ReactNode } from "react"
import styles from "./identityCard.module.css"
import AddToPhotosOutlinedIcon from "@mui/icons-material/AddToPhotosOutlined"

type IdentityCardProps = {
  title: string
  subtitle?: string
  detail?: ReactNode
  imageSrc?: string
  onAddToCollection?: () => void
}

export default function IdentityCard({
  title,
  subtitle,
  detail,
  imageSrc,
  onAddToCollection
}: IdentityCardProps) {
  return (
    <div className={styles.identityCard}>
      <IconButton
        aria-label="add to collection"
        size="small"
        color="inherit"
        sx={{ position: "absolute", top: 16, right: 16 }}
        onClick={onAddToCollection}
      >
        <AddToPhotosOutlinedIcon sx={{ width: 16, height: 16 }} />
      </IconButton>

      <Avatar sx={{ width: 88, height: 88 }} src={imageSrc || "/broken-image.jpg"} />

      <div>
        <Typography variant="subtitle1" component="h1" fontWeight="bold">
          {title}
        </Typography>

        {subtitle && <Typography variant="body2">{subtitle}</Typography>}

        {detail && <Typography variant="body2">{detail}</Typography>}
      </div>
    </div>
  )
}
