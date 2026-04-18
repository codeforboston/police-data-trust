"use client"

import { useParams } from "next/navigation"
import OrganizationProfile from "@/components/Profile/OrganizationProfile"
import { useOrganization } from "@/utils/useProfile"

export default function SourcePage() {
  const params = useParams<{ identifier: string }>()
  const identifier = params.identifier
  const { profile: organization, loading } = useOrganization(identifier)

  if (loading) {
    return <div className="p-4">Loading organization...</div>
  }

  if (!organization) {
    return <div className="p-4">Organization not found.</div>
  }

  return <OrganizationProfile organization={organization} />
}
