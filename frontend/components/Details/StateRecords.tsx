import { Typography } from "@mui/material"
import { Officer } from "@/utils/api"
import DetailCard from "./DetailCard"

export default function StateRecords({ officer }: { officer: Officer }) {
  return (
    <>
      <Typography variant="body1" sx={{ marginTop: "32px", marginBottom: "16px" }}>
        State records
      </Typography>
      <DetailCard>
        {officer.state_ids && officer.state_ids.length > 0 ? (
          officer.state_ids.map((state_id, index) => (
            <div key={index}>
              <span style={{ fontWeight: "500" }}>
                {state_id.state} {state_id.id_name}
              </span>
              , {state_id.value}
            </div>
          ))
        ) : (
          <div>No state records available.</div>
        )}
      </DetailCard>
    </>
  )
}
