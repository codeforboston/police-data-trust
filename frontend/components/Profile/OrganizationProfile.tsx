"use client"

import React from "react"
import SuggestionsCard from "@/components/Profile/SuggestionsCard"
import ProfileLayout from "@/components/Profile/ProfileLayout"
import ProfileHeaderCard from "@/components/Profile/ProfileHeaderCard"
import ContactCard from "@/components/Profile/ContactCard"
import OrganizationMembers from "@/components/Profile/OrganizationMembersCard"
import ActivityCard from "@/components/Profile/ActivityCard"
import { Organization } from "@/utils/api"

export default function OrganizationProfile({ organization }: { organization: Organization }) {
  // TODO: Replace with real data
  const peopleSuggestions = [
    { name: "Samuel Smith", title: "Title", avatarUrl: "/broken-image.jpg" },
    { name: "Marian Linehan", title: "Title", avatarUrl: "/broken-image.jpg" },
    { name: "June MacCabe", title: "Title", avatarUrl: "/broken-image.jpg" },
    { name: "Joseph Vanasse", title: "Title", avatarUrl: "/broken-image.jpg" }
  ]

  const orgSuggestions = [
    { name: "Law Firm Name 1", title: "Title", avatarUrl: "/broken-image.jpg" },
    { name: "Law Firm Name 2", title: "Title", avatarUrl: "/broken-image.jpg" },
    { name: "Law Firm Name 3", title: "Title", avatarUrl: "/broken-image.jpg" },
    { name: "Law Firm Name 4", title: "Title", avatarUrl: "/broken-image.jpg" }
  ]

  return (
    <ProfileLayout
      sidebar={
        <>
          <SuggestionsCard title="People you may know" items={peopleSuggestions} />
          <SuggestionsCard title="Organizations you may know" items={orgSuggestions} />
        </>
      }
    >
      <ProfileHeaderCard
        firstName={organization.name}
        lastName=""
        avatarUrl={organization.logo}
        title={organization.type_of_service}
        organization=""
        city={organization.location?.city || ""}
        state={organization.location?.state || ""}
        biography={organization.description}
        isOwnProfile={false}
      />
      <ContactCard
        primaryEmail={organization.email}
        website={organization.website}
        socials={{
          facebook: undefined,
          instagram: undefined,
          linkedin: undefined,
          twitter: undefined,
          youtube: undefined
        }}
        isOwnProfile={false}
      />
      <ActivityCard />
      <OrganizationMembers />
      <div style={{ height: "20px" }} />
    </ProfileLayout>
  )
}
