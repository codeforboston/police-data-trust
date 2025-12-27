"use client"

import React, { useState, useEffect } from "react"
import styles from "../../edit/EditProfilePage.module.css"
import { useUserProfile } from "@/utils/useProfile"
import { TextField, Button, Box, IconButton, Typography } from "@mui/material"
import ArrowBackIcon from "@mui/icons-material/ArrowBack"
import { useRouter } from "next/navigation"

// validation helpers
const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
const isValidUrl = (url: string) => {
  if (!url) return true
  try {
    new URL(url.startsWith("http") ? url : `https://${url}`)
    return true
  } catch {
    return false
  }
}

export default function EditProfileContact() {
  const { profile, loading, updateProfile } = useUserProfile()
  const router = useRouter()

  const [saving, setSaving] = useState(false)

  const [email, setEmail] = useState("")
  const [email2, setEmail2] = useState("")
  const [website, setWebsite] = useState("")
  const [linkedIn, setLinkedIn] = useState("")
  const [facebook, setFacebook] = useState("")
  const [instagram, setInstagram] = useState("")
  const [twitter, setTwitter] = useState("")
  const [youtube, setYoutube] = useState("")

  const [errors, setErrors] = useState({
    email: "",
    email2: "",
    website: "",
    linkedIn: "",
    facebook: "",
    instagram: "",
    twitter: "",
    youtube: ""
  })

  useEffect(() => {
    if (profile) {
      setEmail(profile.primary_email || "")

      setEmail2(profile.contact_info.additional_emails[0])

      setWebsite(profile.website || "")

      const socials = profile.social_media || {}
      setLinkedIn(socials.linkedin_url ?? "")
      setFacebook(socials.facebook_url ?? "")
      setInstagram(socials.instagram_url ?? "")
      setTwitter(socials.twitter_url ?? "")
      setYoutube(socials.youtube_url ?? "")
    }
  }, [profile])

  const validateForm = () => {
    const newErrors = {
      email: "",
      email2: "",
      website: "",
      linkedIn: "",
      facebook: "",
      instagram: "",
      twitter: "",
      youtube: ""
    }

    // primary email must exist and be valid
    if (!email.trim()) {
      newErrors.email = "Primary email is required"
    } else if (!isValidEmail(email)) {
      newErrors.email = "Enter a valid email address"
    }

    // other fields are optional but if present, must be valid
    if (email2 && !isValidEmail(email2)) newErrors.email2 = "Enter a valid secondary email"
    if (website && !isValidUrl(website)) newErrors.website = "Enter a valid website URL"
    if (linkedIn && !isValidUrl(linkedIn)) newErrors.linkedIn = "Enter a valid LinkedIn URL"
    if (facebook && !isValidUrl(facebook)) newErrors.facebook = "Enter a valid Facebook URL"
    if (instagram && !isValidUrl(instagram)) newErrors.instagram = "Enter a valid Instagram URL"
    if (twitter && !isValidUrl(twitter)) newErrors.twitter = "Enter a valid Twitter URL"
    if (youtube && !isValidUrl(youtube)) newErrors.youtube = "Enter a valid YouTube URL"

    setErrors(newErrors)
    return Object.values(newErrors).every((msg) => msg === "")
  }

  const handleSubmit = async () => {
    if (!validateForm()) return

    setSaving(true)
    try {
      if (profile) {
        const payload = {
          primary_email: email,
          secondary_emails: email2 ? [{ email: email2 }] : [],
          website: website || "",
          social_media_contacts: {
            linkedin_url: linkedIn || "",
            facebook_url: facebook || "",
            instagram_url: instagram || "",
            twitter_url: twitter || "",
            youtube_url: youtube || ""
          }
        }

        await updateProfile(payload)

        router.push("/profile")
      }
    } catch (e) {
      console.error("Failed to update profile:", e)
      alert("Failed to update profile.")
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <p>Loading...</p>
  if (!profile) return <p>Unable to load profile.</p>

  return (
    <div className={styles.container}>
      <div>
        <IconButton aria-label="back to profile" href="/profile" sx={{ color: "#000" }}>
          <ArrowBackIcon />
        </IconButton>
      </div>

      <Box component="form" sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
        <div className={styles.section}>
          <Typography variant="h6">Contact Info</Typography>

          <TextField
            label="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="e.g. john@email.com"
            error={!!errors.email}
            helperText={errors.email}
            required
          />

          <TextField
            label="Secondary Email"
            value={email2 || ""}
            onChange={(e) => setEmail2(e.target.value)}
            placeholder="e.g. john@email.com"
            error={!!errors.email2}
            helperText={errors.email2}
          />

          <TextField
            label="Website"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
            placeholder="e.g. www.website.com"
            error={!!errors.website}
            helperText={errors.website}
          />
        </div>

        <div className={styles.section}>
          <Typography variant="h6">Social Media Links</Typography>

          <TextField
            label="LinkedIn Link"
            value={linkedIn}
            onChange={(e) => setLinkedIn(e.target.value)}
            placeholder="linkedin.com/"
            error={!!errors.linkedIn}
            helperText={errors.linkedIn}
          />
          <TextField
            label="Facebook Link"
            value={facebook}
            onChange={(e) => setFacebook(e.target.value)}
            placeholder="facebook.com/"
            error={!!errors.facebook}
            helperText={errors.facebook}
          />
          <TextField
            label="Instagram Link"
            value={instagram}
            onChange={(e) => setInstagram(e.target.value)}
            placeholder="instagram.com/"
            error={!!errors.instagram}
            helperText={errors.instagram}
          />
          <TextField
            label="X - Twitter Link"
            value={twitter}
            onChange={(e) => setTwitter(e.target.value)}
            placeholder="x.com/"
            error={!!errors.twitter}
            helperText={errors.twitter}
          />
          <TextField
            label="YouTube Link"
            value={youtube}
            onChange={(e) => setYoutube(e.target.value)}
            placeholder="youtube.com/"
            error={!!errors.youtube}
            helperText={errors.youtube}
          />
        </div>

        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? "Saving..." : "Save Changes"}
        </Button>
      </Box>
    </div>
  )
}
