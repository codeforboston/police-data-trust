"use client"

import React, { useState, useEffect } from "react"
import styles from "./EditProfilePage.module.css"
import { useUserProfile } from "@/utils/useProfile"
import { useRouter } from "next/navigation"
import { US_STATES } from "@/utils/constants"
import {
  TextField,
  Button,
  Box,
  IconButton,
  Avatar,
  Typography,
  FormControl,
  MenuItem,
  Select,
  InputLabel
} from "@mui/material"
import ArrowBackIcon from "@mui/icons-material/ArrowBack"
import { UpdateUserProfilePayload, UserProfile } from "@/utils/api"

export default function EditProfilePage() {
  const { profile, loading, updateProfile } = useUserProfile()
  const [saving, setSaving] = useState(false)

  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [organization, setOrganization] = useState("")
  const [primaryPosition, setPrimaryPosition] = useState("")
  const [city, setCity] = useState("")
  const [state, setState] = useState("")
  const [biography, setBiography] = useState("")

  const [errors, setErrors] = useState({
    firstName: "",
    lastName: "",
    organization: "",
    primaryPosition: "",
    city: "",
    state: "",
    biography: ""
  })

  const router = useRouter()

  useEffect(() => {
    if (profile) {
      setFirstName(profile.first_name)
      setLastName(profile.last_name)
      setOrganization(profile.employment?.employer || "")
      setPrimaryPosition(profile.employment?.title || "")
      setCity(profile.location?.city || "")
      setState(profile.location?.state || "")
      setBiography(profile.bio || "")
    }
  }, [profile])

  const validateForm = () => {
    const newErrors: typeof errors = {
      firstName: firstName.trim() ? "" : "Please enter a first name",
      lastName: lastName.trim() ? "" : "Please enter a last name",
      organization: organization.trim() ? "" : "Please enter an employer",
      primaryPosition: primaryPosition.trim() ? "" : "Please enter a primary position",
      city: city.trim() ? "" : "Please enter a city",
      state: state.trim() ? "" : "Please enter a state",
      biography: biography.length <= 1000 ? "" : "Bio must be 1,000 characters or less"
    }

    setErrors(newErrors)

    return Object.values(newErrors).every((msg) => msg === "")
  }

  const handleSubmit = async () => {
    if (!validateForm()) return

    setSaving(true)
    try {
      if (profile) {
        const payload: UpdateUserProfilePayload = {
          first_name: firstName,
          last_name: lastName,
          bio: biography,
          employment: {
            employer: organization,
            title: primaryPosition
          },
          location: {
            city: city,
            state: state
          }
        }

        await updateProfile(payload as Partial<UserProfile>)
        router.push("/profile")
      }
    } catch (e) {
      console.error("Profile update failed", e)
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

      <div className={styles.avatarRow}>
        <Avatar sx={{ width: 160, height: 160 }} src="/broken-image.jpg" />
        <Button variant="outlined">Change photo</Button>
      </div>

      <Box component="form" sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
        <div className={styles.section}>
          <Typography variant="h6">Edit Personal Information</Typography>
          <TextField
            label="First Name"
            required
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            error={!!errors.firstName}
            helperText={errors.firstName}
          />
          <TextField
            label="Last Name"
            required
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            error={!!errors.lastName}
            helperText={errors.lastName}
          />
        </div>

        <div className={styles.section}>
          <Typography variant="h6">Current Employment</Typography>
          <TextField
            label="Primary Position"
            required
            value={primaryPosition}
            onChange={(e) => setPrimaryPosition(e.target.value)}
            error={!!errors.primaryPosition}
            helperText={errors.primaryPosition}
          />
          <TextField
            label="Employer"
            required
            value={organization}
            onChange={(e) => setOrganization(e.target.value)}
            error={!!errors.organization}
            helperText={errors.organization}
          />
        </div>

        <div className={styles.section}>
          <Typography variant="h6">Location</Typography>
          <TextField
            label="City"
            required
            value={city}
            onChange={(e) => setCity(e.target.value)}
            error={!!errors.city}
            helperText={errors.city}
          />
          <FormControl size="medium" variant="outlined" fullWidth>
            <InputLabel id="select-state" required>
              State
            </InputLabel>
            <Select
              labelId="select-state"
              label="State"
              value={state}
              onChange={(e) => setState(e.target.value)}
            >
              <MenuItem value="" disabled>
                Select state
              </MenuItem>
              {US_STATES.map(({ name, abbreviation }) => (
                <MenuItem key={abbreviation} value={abbreviation}>
                  {name}
                </MenuItem>
              ))}
            </Select>
            {errors.state && (
              <Typography variant="caption" color="error">
                {errors.state}
              </Typography>
            )}
          </FormControl>
        </div>

        <div className={styles.section}>
          <Typography variant="h6">Bio</Typography>
          <div className={styles.bioWrapper}>
            <TextField
              value={biography}
              placeholder="Use this space to write a short bio about yourself in 1,000 characters or less..."
              multiline
              fullWidth
              onChange={(e) => setBiography(e.target.value)}
              error={!!errors.biography}
            />
            <p
              className={
                biography.length > 1000 ? styles.biographyCountError : styles.biographyCount
              }
            >
              {biography.length}/1000
            </p>
          </div>
        </div>

        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? "Saving..." : "Save Changes"}
        </Button>
      </Box>
    </div>
  )
}
