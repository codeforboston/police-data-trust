"use client"

import { useSearchParams } from "next/navigation"
import { Box, Typography } from "@mui/material"

export default function SearchPage() {
  const searchParams = useSearchParams()
  const query = searchParams.get("query") || ""

  return (
    <Box sx={{ padding: "20px" }}>
      <Typography variant="h4" gutterBottom>
        Search Results for "{query}" 
        More to come!
      </Typography>
    </Box>
  )
}