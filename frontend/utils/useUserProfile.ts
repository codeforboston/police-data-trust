import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { UserProfile, UpdateUserProfilePayload } from "./api"

export const useUserProfile = () => {
  const { hasHydrated, accessToken } = useAuth()
  const router = useRouter()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)

  // fetch current user profile
  useEffect(() => {
    if (!hasHydrated) return
    if (!accessToken) {
      router.push("/login")
      return
    }

    const fetchProfile = async () => {
      const res = await apiFetch(`${apiBaseUrl}${API_ROUTES.users.self}`)
      if (!res.ok) {
        router.push("/login")
        return
      }

      const data: UserProfile = await res.json()

      setProfile(data)
      setLoading(false)
    }

    fetchProfile()
  }, [hasHydrated, accessToken, router])

  // Update user profile
  const updateProfile = async (
    updates: {
      secondary_emails?: { email: string }[]
      phone_contacts?: { phone_number: string }[]
      social_media_contacts?: UpdateUserProfilePayload["social_media"]
      website?: string
    } & Partial<UserProfile>
  ) => {
    if (!accessToken) throw new Error("No access token")

    const { secondary_emails, phone_contacts, social_media_contacts, website, ...rest } = updates

    const transformedUpdates: UpdateUserProfilePayload = {
      ...rest,
      contact_info: {
        additional_emails: secondary_emails?.map((e) => e.email) || [],
        phone_numbers: phone_contacts?.map((p) => p.phone_number) || []
      },
      website,
      social_media: social_media_contacts
    }

    const res = await apiFetch(`${apiBaseUrl}${API_ROUTES.users.self}`, {
      method: "PATCH",
      body: JSON.stringify(transformedUpdates),
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      }
    })

    if (!res.ok) {
      const errorText = await res.text()
      console.error("Profile update failed:", errorText)
      throw new Error("Failed to update profile")
    }

    const updatedProfile: UserProfile = await res.json()
    setProfile(updatedProfile)
    return updatedProfile
  }

  return { profile, loading, updateProfile }
}
