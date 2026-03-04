import { Avatar, Link, Typography } from "@mui/material"
import styles from "./contentDetails.module.css"

type ContentDetailsItem = {
  label: string
  value: string
}

type AssociatedPerson = {
  name: string
  imageSrc?: string
  href?: string
}

type ContentDetailsProps = {
  contentType: string
  dataSources: string[]
  lastUpdatedText?: string
  lastUpdatedBy?: string
  lastUpdatedByImageSrc?: string
  summaryItems?: ContentDetailsItem[]
  associatedTitle?: string
  associatedPeople?: AssociatedPerson[]
  associatedHref?: string
}

export default function ContentDetails({
  contentType,
  dataSources,
  lastUpdatedText,
  lastUpdatedBy,
  lastUpdatedByImageSrc,
  summaryItems = [],
  associatedTitle = "Associated people",
  associatedPeople = [],
  associatedHref
}: ContentDetailsProps) {
  return (
    <div className={styles.sidebarContent}>
      <Typography variant="subtitle1" fontWeight={600}>
        Content Details
      </Typography>

      <div>
        <Typography variant="subtitle1" fontWeight={600} fontSize={14} color="text.secondary">
          Content type
        </Typography>
        <Typography variant="body2" color="#475467">
          {contentType}
        </Typography>
      </div>

      <div>
        <Typography variant="subtitle1" fontWeight={600} fontSize={14} color="text.secondary">
          Data sources
        </Typography>
        {dataSources.length > 0 ? (
          dataSources.map((source, index) => (
            <Typography key={index} variant="body2" color="#475467">
              {source}
            </Typography>
          ))
        ) : (
          <Typography variant="body2" color="#475467">
            No sources available
          </Typography>
        )}
      </div>

      <div>
        <Typography variant="subtitle1" fontWeight={600} fontSize={14} color="text.secondary">
          Last updated
        </Typography>

        {lastUpdatedText || lastUpdatedBy ? (
          <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
            {lastUpdatedText && (
              <Typography variant="body2" color="#475467">
                {lastUpdatedText}
              </Typography>
            )}

            {lastUpdatedBy && (
              <>
                <Avatar
                  sx={{ width: 16, height: 16 }}
                  src={lastUpdatedByImageSrc || "/broken-image.jpg"}
                />
                <Typography variant="caption" fontWeight={500} color="#000000">
                  {lastUpdatedBy}
                </Typography>
              </>
            )}
          </div>
        ) : (
          <Typography variant="body2" color="#475467">
            Unknown
          </Typography>
        )}
      </div>

      {summaryItems.length > 0 && (
        <div>
          <Typography variant="subtitle1" fontWeight={600} fontSize={14} sx={{ marginTop: "10px" }}>
            Summary
          </Typography>

          {summaryItems.map((item, index) => (
            <Typography key={index} variant="body2" color="#475467">
              {item.value} {item.label}
            </Typography>
          ))}
        </div>
      )}

      {associatedPeople.length > 0 && (
        <div className={styles.associatedContainer}>
          <Typography variant="subtitle1" fontWeight={600} fontSize={14} sx={{ marginTop: "10px" }}>
            {associatedTitle}
          </Typography>

          {associatedPeople.map((person, index) => (
            <div key={index} className={styles.associatedOfficer}>
              <Avatar sx={{ width: 32, height: 32 }} src={person.imageSrc || "/broken-image.jpg"} />
              <Typography variant="caption" fontWeight={500} color="#000000">
                {person.name}
              </Typography>
            </div>
          ))}

          {associatedHref && (
            <Link href={associatedHref} underline="none" variant="body2" color="text.secondary">
              View all
            </Link>
          )}
        </div>
      )}
    </div>
  )
}