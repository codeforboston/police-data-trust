import { Chip, Typography } from "@mui/material"
import DetailCard from "./DetailCard"

// TODO: add award data when available
export default function Awards() {
  return (
    <>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "16px",
          marginTop: "32px",
          marginBottom: "16px"
        }}
      >
        <Typography component="h2" variant="h5" sx={{ fontSize: "1.3rem", fontWeight: "500" }}>
          Awards
        </Typography>
        <Chip label="0" />
      </div>
      <DetailCard>
        <div>No awards available.</div>
      </DetailCard>
    </>
  )
}
