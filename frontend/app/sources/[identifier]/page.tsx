"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import OrganizationProfile from "@/components/Profile/OrganizationProfile"
import { useOrganization } from "@/utils/useProfile"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { SourceActivity, SourceMember } from "@/utils/api"
import { useUserProfile } from "@/utils/useProfile"

export default function SourcePage() {
  const params = useParams<{ identifier: string }>()
  const identifier = params.identifier
  const { profile: organization, loading } = useOrganization(identifier)
  const { profile: currentUser } = useUserProfile()
  const { accessToken } = useAuth()
  const [members, setMembers] = useState<SourceMember[]>([])
  const [activity, setActivity] = useState<SourceActivity | null>(null)

  useEffect(() => {
    if (!accessToken || !organization?.uid) return

    apiFetch(`${apiBaseUrl}${API_ROUTES.sources.members(organization.uid)}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load source members")
        }

        return res.json()
      })
      .then((data) => setMembers(data.results || data))
      .catch((error) => {
        console.error(error)
        setMembers([])
      })
  }, [accessToken, organization?.uid])

  useEffect(() => {
    if (!accessToken || !organization?.uid) return

    apiFetch(`${apiBaseUrl}${API_ROUTES.sources.activity(organization.uid)}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load source activity")
        }

        return res.json()
      })
      .then((data) => setActivity(data))
      .catch((error) => {
        console.error(error)
        setActivity(null)
      })
  }, [accessToken, organization?.uid])

  if (loading) {
    return <div className="p-4">Loading organization...</div>
  }

  if (!organization) {
    return <div className="p-4">Organization not found.</div>
  }

  const canEdit =
    !!currentUser?.uid &&
    organization.memberships?.some(
      (membership) => membership.uid === currentUser.uid && membership.role === "Administrator"
    ) === true

  return (
    <OrganizationProfile
      organization={organization}
      members={members}
      canEdit={canEdit}
      activity={activity}
    />
  )
}
