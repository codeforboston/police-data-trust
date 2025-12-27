import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { UserProfile, UpdateUserProfilePayload, Organization } from "./api"

// Helper function to generate slug from name
const generateSlug = (firstName: string, lastName?: string): string => {
  const fullName = lastName ? `${firstName} ${lastName}` : firstName
  return fullName
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(".", "-")
    .replace(/[^a-z0-9-]/g, "")
}

type ProfileType = "user" | "organization"

export const useProfile = <T extends UserProfile | Organization>(
  type: ProfileType,
  slug?: string
) => {
  const { hasHydrated, accessToken } = useAuth()
  const router = useRouter()
  const [profile, setProfile] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [isOwnProfile, setIsOwnProfile] = useState(false)

  useEffect(() => {
    if (!hasHydrated || !accessToken) {
      if (!hasHydrated) return
      router.push("/login")
      return
    }

    const fetchProfile = async () => {
      try {
        if (type === "user") {
          let matchedProfile: UserProfile | null = null

          if (slug) {
            // Fetch current user first to check if slug matches them
            const selfRes = await apiFetch(`${apiBaseUrl}${API_ROUTES.users.self}`, {
              headers: {
                Authorization: `Bearer ${accessToken}`
              }
            })

            if (!selfRes.ok) {
              router.push("/login")
              return
            }

            const selfData: UserProfile = await selfRes.json()
            const selfUsername = generateSlug(selfData.first_name, selfData.last_name)

            if (slug === selfUsername) {
              matchedProfile = selfData
              setIsOwnProfile(true)
            } else {
              router.push("/404")
              return
            }
          } else {
            // Fetch current user profile (no slug provided)
            const res = await apiFetch(`${apiBaseUrl}${API_ROUTES.users.self}`, {
              headers: {
                Authorization: `Bearer ${accessToken}`
              }
            })

            if (!res.ok) {
              router.push("/login")
              return
            }

            matchedProfile = await res.json()
            setIsOwnProfile(true)
          }

          setProfile(matchedProfile as T)
        } else if (type === "organization") {
          // Fetch all organizations/sources
          const res = await apiFetch(`${apiBaseUrl}${API_ROUTES.sources.all}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`
            }
          })

          if (!res.ok) {
            if (res.status === 401) {
              router.push("/login")
              return
            }
            throw new Error("Failed to fetch organizations")
          }

          const data = await res.json()
          const sources = data.results || data

          if (!slug) {
            setProfile(null)
            setLoading(false)
            return
          }

          const matchedSource = sources.find(
            (source: { name: string }) => generateSlug(source.name) === slug
          )

          if (!matchedSource) {
            router.push("/404")
            return
          }

          const organization: Organization = {
            uid: matchedSource.uid,
            name: matchedSource.name,
            description: matchedSource.description || "",
            logo: matchedSource.logo || "/broken-image.jpg",
            website: matchedSource.url || "",
            email: matchedSource.contact_email || "",
            location: {
              city: matchedSource.city || "",
              state: matchedSource.state || ""
            },
            type_of_service: matchedSource.type_of_service || "Organization"
          }

          setProfile(organization as T)
        }
      } catch (error) {
        console.error("Error fetching profile:", error)
        router.push("/login")
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [hasHydrated, accessToken, type, slug, router])

  // Update user profile (only works for own profile)
  const updateProfile = async (
    updates: {
      secondary_emails?: { email: string }[]
      phone_contacts?: { phone_number: string }[]
      social_media_contacts?: UpdateUserProfilePayload["social_media"]
      website?: string
    } & Partial<UserProfile>
  ) => {
    if (!accessToken) throw new Error("No access token")
    if (!isOwnProfile) throw new Error("Cannot update another profile")
    if (type !== "user") throw new Error("Only user profiles can be updated")

    const { secondary_emails, phone_contacts, social_media_contacts, website, ...rest } = updates

    const transformedUpdates: UpdateUserProfilePayload = {
      ...rest,
      contact_info: {
        additional_emails: secondary_emails?.map((e) => e.email) || [],
        phone_numbers: phone_contacts?.map((p) => p.phone_number) || []
      },
      website,
      social_media: social_media_contacts,
      location: updates.location
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
    setProfile(updatedProfile as T)
    return updatedProfile
  }

  return { profile, loading, updateProfile, isOwnProfile }
}

export const useUserProfile = (slug?: string) => useProfile<UserProfile>("user", slug)
export const useOrganization = (slug?: string) => useProfile<Organization>("organization", slug)
