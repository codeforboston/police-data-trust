import React from "react"
import { Card, CardContent, Typography } from "@mui/material"

export default function ActivityCard() {
  return (
    <Card variant="outlined" sx={{ marginTop: "20px", marginBottom: "20px" }}>
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
          },
          display: "flex",
          flexDirection: "column",
          alignItems: "center"
        }}
      >
        <Typography variant="h5" fontWeight={600}>
          Activity
        </Typography>
        <Typography variant="body1" sx={{ marginTop: "8px", color: "#757575" }}>
          Last active Oct 24, 2025
        </Typography>
        {/* TODO: Add contribution history and location data viz */}
      </CardContent>
    </Card>
  )
}
