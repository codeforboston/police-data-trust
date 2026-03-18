import * as React from "react"
import { Box, SxProps, Theme } from "@mui/material"

interface DetailCardProps {
  children: React.ReactNode
  sx?: SxProps<Theme>
}

export default function DetailCard({ children, sx }: DetailCardProps) {
  return (
    <Box
      sx={{
        padding: "16px",
        border: "1px solid #B3B3B3",
        borderRadius: "16px",
        display: "flex",
        flexDirection: "column",
        gap: "16px",
        ...sx
      }}
    >
      {children}
    </Box>
  )
}
