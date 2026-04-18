"use client"

import React, { useEffect, useMemo, useState } from "react"
import styles from "../../../profile/edit/EditProfilePage.module.css"
import { useParams, useRouter } from "next/navigation"
import ArrowBackIcon from "@mui/icons-material/ArrowBack"
import { Box, Button, IconButton, TextField, Typography } from "@mui/material"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { useOrganization, useUserProfile } from "@/utils/useProfile"
import { UpdateOrganizationPayload } from "@/utils/api"

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

export default function EditSourcePage() {
  const params = useParams<{ identifier: string }>()
  const identifier = params.identifier
  const router = useRouter()
  const { profile: organization, loading } = useOrganization(identifier)
  const { profile: currentUser, loading: userLoading } = useUserProfile()
  const [saving, setSaving] = useState(false)

  const [name, setName] = useState("")
  const [slug, setSlug] = useState("")
  const [email, setEmail] = useState("")
  const [website, setWebsite] = useState("")
  const [description, setDescription] = useState("")
  const [linkedIn, setLinkedIn] = useState("")
  const [facebook, setFacebook] = useState("")
  const [instagram, setInstagram] = useState("")
  const [twitter, setTwitter] = useState("")
  const [youtube, setYoutube] = useState("")

  const [errors, setErrors] = useState({
    name: "",
    slug: "",
    email: "",
    website: "",
    description: "",
    linkedIn: "",
    facebook: "",
    instagram: "",
    twitter: "",
    youtube: ""
  })

  const canEdit = useMemo(
    () =>
      !!currentUser?.uid &&
      organization?.memberships?.some(
        (membership) => membership.uid === currentUser.uid && membership.role === "Administrator"
      ) === true,
    [currentUser?.uid, organization?.memberships]
  )

  useEffect(() => {
    if (organization) {
      setName(organization.name || "")
      setSlug(organization.slug || "")
      setEmail(organization.email || "")
      setWebsite(organization.website || "")
      setDescription(organization.description || "")
      setLinkedIn(organization.social_media?.linkedin_url || "")
      setFacebook(organization.social_media?.facebook_url || "")
      setInstagram(organization.social_media?.instagram_url || "")
      setTwitter(organization.social_media?.twitter_url || "")
      setYoutube(organization.social_media?.youtube_url || "")
    }
  }, [organization])

  useEffect(() => {
    if (!loading && !userLoading && organization && !canEdit) {
      router.replace(organization.uid ? `/sources/${organization.uid}` : "/404")
    }
  }, [canEdit, loading, organization, router, userLoading])

  const validateForm = () => {
    const newErrors = {
      name: name.trim() ? "" : "Organization name is required",
      slug: slug.trim() ? "" : "Slug is required",
      email: !email.trim() ? "Primary email is required" : !isValidEmail(email) ? "Enter a valid email address" : "",
      website: website && !isValidUrl(website) ? "Enter a valid website URL" : "",
      description:
        description.length > 500 ? "Description must be 500 characters or less" : "",
      linkedIn: linkedIn && !isValidUrl(linkedIn) ? "Enter a valid LinkedIn URL" : "",
      facebook: facebook && !isValidUrl(facebook) ? "Enter a valid Facebook URL" : "",
      instagram: instagram && !isValidUrl(instagram) ? "Enter a valid Instagram URL" : "",
      twitter: twitter && !isValidUrl(twitter) ? "Enter a valid Twitter URL" : "",
      youtube: youtube && !isValidUrl(youtube) ? "Enter a valid YouTube URL" : ""
    }

    setErrors(newErrors)
    return Object.values(newErrors).every((msg) => msg === "")
  }

  const handleSubmit = async () => {
    if (!organization?.uid || !validateForm()) return

    setSaving(true)
    try {
      const payload: UpdateOrganizationPayload = {
        name,
        slug,
        contact_email: email,
        url: website,
        description,
        social_media: {
          linkedin_url: linkedIn || "",
          facebook_url: facebook || "",
          instagram_url: instagram || "",
          twitter_url: twitter || "",
          youtube_url: youtube || ""
        }
      }

      const res = await apiFetch(`${apiBaseUrl}${API_ROUTES.sources.profile(organization.uid)}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      })

      if (!res.ok) {
        throw new Error("Failed to update source")
      }

      const updated = await res.json()
      router.push(`/sources/${updated.slug || updated.uid}`)
    } catch (e) {
      console.error("Source update failed", e)
      alert("Failed to update organization.")
    } finally {
      setSaving(false)
    }
  }

  if (loading || userLoading) return <p>Loading...</p>
  if (!organization) return <p>Unable to load organization.</p>
  if (!canEdit) return <p>Checking permissions...</p>

  return (
    <div className={styles.container}>
      <div>
        <IconButton
          aria-label="back to organization"
          href={organization.uid ? `/sources/${organization.uid}` : "/sources"}
          sx={{ color: "#000" }}
        >
          <ArrowBackIcon />
        </IconButton>
      </div>

      <Box component="form" sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
        <div className={styles.section}>
          <Typography variant="h6">Organization Details</Typography>

          <TextField
            label="Organization Name"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            error={!!errors.name}
            helperText={errors.name}
          />

          <TextField
            label="Slug"
            required
            value={slug}
            onChange={(e) => setSlug(e.target.value)}
            error={!!errors.slug}
            helperText={errors.slug}
          />

          <TextField
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            error={!!errors.description}
            helperText={errors.description || `${description.length}/500`}
            multiline
            minRows={4}
          />
        </div>

        <div className={styles.section}>
          <Typography variant="h6">Contact Info</Typography>

          <TextField
            label="Email Address"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            error={!!errors.email}
            helperText={errors.email}
          />

          <TextField
            label="Website"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
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
            error={!!errors.linkedIn}
            helperText={errors.linkedIn}
          />
          <TextField
            label="Facebook Link"
            value={facebook}
            onChange={(e) => setFacebook(e.target.value)}
            error={!!errors.facebook}
            helperText={errors.facebook}
          />
          <TextField
            label="Instagram Link"
            value={instagram}
            onChange={(e) => setInstagram(e.target.value)}
            error={!!errors.instagram}
            helperText={errors.instagram}
          />
          <TextField
            label="X - Twitter Link"
            value={twitter}
            onChange={(e) => setTwitter(e.target.value)}
            error={!!errors.twitter}
            helperText={errors.twitter}
          />
          <TextField
            label="YouTube Link"
            value={youtube}
            onChange={(e) => setYoutube(e.target.value)}
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
