"use client"

import React from "react"
import { useUserProfile } from "@/utils/useUserProfile"
import SuggestionsCard from "@/components/Profile/SuggestionsCard"
import ProfileLayout from "@/components/Profile/ProfileLayout"
import ProfileHeaderCard from "@/components/Profile/ProfileHeaderCard"
import OrganizationCard from "@/components/Profile/OrganizationCard"
import ContactCard from "@/components/Profile/ContactCard"
import { SocialMedia } from "@/utils/api"

export default function ProfilePage() {
  const { profile, loading } = useUserProfile()

  if (loading) return <p>Loading profile...</p>
  if (!profile) return <p>Unable to load profile.</p>

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

  const socialMediaContacts = profile.social_media || ({} as SocialMedia)

  return (
    <ProfileLayout
      sidebar={
        <>
          <SuggestionsCard title="People you may know" items={peopleSuggestions} />
          <SuggestionsCard title="Organizations you may know" items={orgSuggestions} />
        </>
      }>
      <ProfileHeaderCard
        firstName={profile.first_name}
        lastName={profile.last_name}
        avatarUrl={profile.profile_image}
        title={profile.employment?.title || ""}
        organization={profile.employment?.employer || ""}
        city={profile.location?.city || ""}
        state={profile.location?.state || ""}
        biography={profile.bio || ""}
        isOwnProfile={true}
      />
      <OrganizationCard />
      <ContactCard
        primaryEmail={profile.primary_email || ""}
        secondaryEmail={profile.contact_info.additional_emails[0]}
        website={profile.website || undefined}
        socials={{
          facebook: socialMediaContacts.facebook_url || undefined,
          instagram: socialMediaContacts.instagram_url || undefined,
          linkedin: socialMediaContacts.linkedin_url || undefined,
          twitter: socialMediaContacts.twitter_url || undefined,
          youtube: socialMediaContacts.youtube_url || undefined
        }}
      />
    </ProfileLayout>
  )
}
