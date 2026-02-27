import { Avatar, Link, Typography } from "@mui/material"
import { Officer } from "@/utils/api"
import styles from "./contentDetails.module.css"

interface ContentDetailsProps {
  officer: Officer
}

// TODO: Replace associated officers and last updated with actual data
export default function ContentDetails({ officer }: ContentDetailsProps) {
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
          Officer
        </Typography>
      </div>

      <div>
        <Typography variant="subtitle1" fontWeight={600} fontSize={14} color="text.secondary">
          Data sources
        </Typography>
        {officer.sources && officer.sources.length > 0 ? (
          officer.sources.map((source, index) => (
            <Typography key={index} variant="body2" color="#475467">
              {source.name}
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

        <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
          <Typography variant="body2" color="#475467">
            Nov 1, 2024 by
          </Typography>
          <Avatar sx={{ width: 16, height: 16 }} src={"/broken-image.jpg"} />
          <Typography variant="caption" fontWeight={500} color="#000000">
            Adam Zelitzky
          </Typography>
        </div>
      </div>

      <div>
        <Typography variant="subtitle1" fontWeight={600} fontSize={14} sx={{ marginTop: "10px" }}>
          Summary
        </Typography>
        <Typography variant="body2" color="#475467">
          {officer.allegation_summary?.reduce((sum, a) => sum + a.complaint_count, 0) || 0}{" "}
          Complaints
        </Typography>
        <Typography variant="body2" color="#475467">
          {officer.allegation_summary?.reduce((sum, a) => sum + a.count, 0) || 0} Allegations
        </Typography>
        <Typography variant="body2" color="#475467">
          {officer.allegation_summary?.reduce((sum, a) => sum + a.substantiated_count, 0) || 0}{" "}
          Substantiated
        </Typography>
        <Typography variant="body2" color="#475467">
          0 Awards
        </Typography>
        <Typography variant="body2" color="#475467">
          0 Related Articles
        </Typography>
      </div>

      <div className={styles.associatedContainer}>
        <Typography variant="subtitle1" fontWeight={600} fontSize={14} sx={{ marginTop: "10px" }}>
          Associated officers
        </Typography>
        <div className={styles.associatedOfficer}>
          <Avatar sx={{ width: 32, height: 32 }} src={"/broken-image.jpg"} />
          <Typography variant="caption" fontWeight={500} color="#000000">
            Adam Zelitzky
          </Typography>
        </div>
        <div className={styles.associatedOfficer}>
          <Avatar sx={{ width: 32, height: 32 }} src={"/broken-image.jpg"} />
          <Typography variant="caption" fontWeight={500} color="#000000">
            Andrew Damora
          </Typography>
        </div>
        <div className={styles.associatedOfficer}>
          <Avatar sx={{ width: 32, height: 32 }} src={"/broken-image.jpg"} />
          <Typography variant="caption" fontWeight={500} color="#000000">
            John Dadamo
          </Typography>
        </div>
        <Link href="#" underline="none" variant="body2" color="text.secondary">
          View all
        </Link>
      </div>
    </div>
  )
}
