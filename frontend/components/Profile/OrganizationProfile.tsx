"use client"

import React from "react"
import ProfileLayout from "@/components/Profile/ProfileLayout"
import ProfileHeaderCard from "@/components/Profile/ProfileHeaderCard"
import ContactCard from "@/components/Profile/ContactCard"
import OrganizationMembers from "@/components/Profile/OrganizationMembersCard"
import ActivityCard from "@/components/Profile/ActivityCard"
import { Organization, SourceActivity, SourceMember } from "@/utils/api"

export default function OrganizationProfile({
  organization,
  members,
  canEdit = false,
  activity
}: {
  organization: Organization
  members: SourceMember[]
  canEdit?: boolean
  activity?: SourceActivity | null
}) {
  return (
    <ProfileLayout>
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
        canEdit={canEdit}
        editHref={organization.uid ? `/sources/${organization.uid}/edit` : undefined}
        showFollowerStats={false}
      />
      <ContactCard
        primaryEmail={organization.email}
        website={organization.website}
        socials={{
          facebook: organization.social_media?.facebook_url,
          instagram: organization.social_media?.instagram_url,
          linkedin: organization.social_media?.linkedin_url,
          twitter: organization.social_media?.twitter_url,
          youtube: organization.social_media?.youtube_url
        }}
        isOwnProfile={false}
        canEdit={canEdit}
        editHref={organization.uid ? `/sources/${organization.uid}/edit` : undefined}
      />
      <ActivityCard activity={activity || null} />
      <OrganizationMembers members={members} />
      <div style={{ height: "20px" }} />
    </ProfileLayout>
  )
}
