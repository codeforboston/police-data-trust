import React from "react"
import Link from "next/link"
import { Avatar, Card, CardContent, Typography } from "@mui/material"
import { UserMembership } from "@/utils/api"
import styles from "./organizationCard.module.css"

const formatJoinedDate = (dateJoined?: string) => {
  if (!dateJoined) return null

  const date = new Date(dateJoined)
  if (Number.isNaN(date.getTime())) return null

  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  })
}

export default function OrganizationCard({ memberships }: { memberships?: UserMembership[] }) {
  if (!memberships?.length) {
    return null
  }

  return (
    <Card variant="outlined" sx={{ marginTop: "20px" }}>
      <CardContent
        sx={{
          p: "40px",
          "&:last-child": {
            pb: "40px"
          },
          "@media (max-width:430px)": {
            p: "24px",
            "&:last-child": {
              pb: "24px"
            }
          }
        }}
      >
        <Typography variant="h5" fontWeight={600}>
          Source Affiliation
        </Typography>

        {memberships.map((membership) => {
          const joinedDate = formatJoinedDate(membership.date_joined)

          return (
            <div key={`${membership.source.uid}-${membership.role || "member"}`}>
              <div className={styles.container}>
                <Link
                  href={
                    membership.source.slug
                      ? `/sources/${membership.source.slug}`
                      : `/sources/${membership.source.uid}`
                  }
                >
                  <Avatar sx={{ width: 40, height: 40 }} src={"/broken-image.jpg"} />
                </Link>
                <div className={styles.containerText}>
                  <Link
                    href={
                      membership.source.slug
                        ? `/sources/${membership.source.slug}`
                        : `/sources/${membership.source.uid}`
                    }
                    className={styles.sourceLink}
                  >
                    <Typography fontWeight={500} fontSize={20}>
                      {membership.source.name}
                    </Typography>
                  </Link>
                  {membership.source.description ? (
                    <Typography>{membership.source.description}</Typography>
                  ) : null}
                  {membership.role ? (
                    <Typography color="text.secondary">{membership.role}</Typography>
                  ) : null}
                </div>
              </div>
              {joinedDate ? (
                <Typography color="text.secondary">Joined on {joinedDate}</Typography>
              ) : null}
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
