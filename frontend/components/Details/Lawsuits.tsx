import { Chip, Typography } from "@mui/material"
import DetailCard from "./DetailCard"

// TODO: add lawsuit data when available
export default function Lawsuits() {
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
          Lawsuits
        </Typography>
        <Chip label="0" />
      </div>
      <DetailCard>
        <div>No lawsuits available.</div>
      </DetailCard>
    </>
  )
}
