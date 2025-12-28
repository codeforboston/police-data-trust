"use client"

import React, { useEffect, useState } from "react"
import OrganizationProfile from "@/components/Profile/OrganizationProfile"
import { useOrganization } from "@/utils/useProfile"
import { useAuth } from "@/providers/AuthProvider"
import { apiFetch } from "@/utils/apiFetch"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { Organization } from "@/utils/api"
import { useSearchParams } from "next/navigation"

export default function OrganizationPage() {
  const searchParams = useSearchParams()
  const slug = searchParams.get("slug")
  const { profile: organization, loading } = useOrganization(slug || "")
  const { accessToken } = useAuth()
  const [allOrgs, setAllOrgs] = useState<Organization[]>([])

  useEffect(() => {
    if (accessToken) {
      apiFetch(`${apiBaseUrl}${API_ROUTES.sources.all}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      })
        .then((res) => res.json())
        .then((data) => setAllOrgs(data.results || data))
    }
  }, [accessToken])

  if (loading) {
    return <div className="p-4">Loading organization...</div>
  }

  if (!organization) {
    return (
      <div className="p-4">
        <p>Organization {slug} not found.</p>
        <p>Available organizations:</p>
        <ul>
          {allOrgs.map((org) => (
            <li key={org.uid}>{org.name}</li>
          ))}
        </ul>
      </div>
    )
  }

  return <OrganizationProfile organization={organization} />
}
