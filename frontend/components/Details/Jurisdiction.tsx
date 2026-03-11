import { Typography } from "@mui/material"
import DetailCard from "./DetailCard"
import Map from "../Map/Map"

// TODO: add jurisdiction data when available
export default function Jurisdiction({
  location
}: {
  location: { latitude: number; longitude: number }
}) {
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
          Jurisdiction
        </Typography>
      </div>
      <DetailCard>
        <Map center={[location.longitude, location.latitude]} zoom={9} />
      </DetailCard>
    </>
  )
}
