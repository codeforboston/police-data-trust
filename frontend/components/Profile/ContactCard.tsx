"use client"

import { Card, CardContent, Typography, IconButton } from "@mui/material"
import ModeEditOutlinedIcon from "@mui/icons-material/ModeEditOutlined"
import EmailIcon from "@mui/icons-material/Email"
import PublicIcon from "@mui/icons-material/Public"
import FacebookIcon from "@mui/icons-material/Facebook"
import InstagramIcon from "@mui/icons-material/Instagram"
import LinkedInIcon from "@mui/icons-material/LinkedIn"
import YouTubeIcon from "@mui/icons-material/YouTube"
import XIcon from "@mui/icons-material/X"
import { useRouter } from "next/navigation"
import styles from "./contactCard.module.css"

interface Props {
  primaryEmail: string
  secondaryEmail?: string
  website?: string
  socials: {
    facebook?: string
    instagram?: string
    linkedin?: string
    twitter?: string
    youtube?: string
  }
  isOwnProfile?: boolean
}

export default function ContactCard({
  primaryEmail,
  secondaryEmail,
  website,
  socials,
  isOwnProfile
}: Props) {
  const router = useRouter()
  const hasSocials = Object.values(socials).some((val) => !!val)

  // normalize website URLs to always include http(s)
  const getSafeUrl = (url: string) => {
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      return `https://${url}`
    }
    return url
  }

  return (
    <Card variant="outlined" sx={{ marginTop: "24px", marginBottom: "24px" }}>
      <CardContent
        sx={{
          p: "40px",
          "&:last-child": { pb: "40px" },
          "@media (max-width:430px)": {
            p: "24px",
            "&:last-child": { pb: "24px" }
          }
        }}
      >
        {isOwnProfile && (
          <IconButton className={styles.editIcon} sx={{ color: "#000" }}>
            <ModeEditOutlinedIcon onClick={() => router.push("/profile/contact/edit")} />
          </IconButton>
        )}

        <Typography variant="h5" fontWeight={600}>
          Contact
        </Typography>

        <div className={styles.contactWrapper}>
          <div className={styles.contactRow}>
            <EmailIcon />
            <div className={styles.contactDetails}>
              <p className={styles.contactLabel}>Email</p>
              <a href={`mailto:${primaryEmail}`} className={styles.emailLink}>
                {primaryEmail}
              </a>
            </div>
          </div>

          {secondaryEmail && (
            <div className={styles.contactRow}>
              <EmailIcon />
              <div className={styles.contactDetails}>
                <p className={styles.contactLabel}>Secondary Email</p>
                <a href={`mailto:${secondaryEmail}`} className={styles.emailLink}>
                  {secondaryEmail}
                </a>
              </div>
            </div>
          )}

          {website && (
            <div className={styles.contactRow}>
              <PublicIcon />
              <div className={styles.contactDetails}>
                <p className={styles.contactLabel}>Website</p>
                <a
                  href={getSafeUrl(website)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={styles.websiteLink}
                >
                  {website}
                </a>
              </div>
            </div>
          )}
        </div>

        {hasSocials && (
          <>
            <Typography variant="h5" fontWeight={600} sx={{ marginTop: "24px" }}>
              Socials
            </Typography>
            <div className={styles.socials}>
              {socials.linkedin && (
                <a href={socials.linkedin} target="_blank" rel="noopener noreferrer">
                  <LinkedInIcon fontSize="large" />
                </a>
              )}
              {socials.facebook && (
                <a href={socials.facebook} target="_blank" rel="noopener noreferrer">
                  <FacebookIcon fontSize="large" />
                </a>
              )}
              {socials.instagram && (
                <a href={socials.instagram} target="_blank" rel="noopener noreferrer">
                  <InstagramIcon fontSize="large" />
                </a>
              )}
              {socials.twitter && (
                <a href={socials.twitter} target="_blank" rel="noopener noreferrer">
                  <XIcon fontSize="large" />
                </a>
              )}
              {socials.youtube && (
                <a href={socials.youtube} target="_blank" rel="noopener noreferrer">
                  <YouTubeIcon fontSize="large" />
                </a>
              )}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
