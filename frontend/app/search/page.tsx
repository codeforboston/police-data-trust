"use client"

import { useSearchParams } from "next/navigation"
import { Box, Typography } from "@mui/material"
import { Suspense } from "react"

export default function SearchPage() {
  return (
    <Box sx={{ padding: "20px" }}>
      <Suspense>
        <QueryName />
      </Suspense>
    </Box>
  )
}

const QueryName = () => {
  const searchParams = useSearchParams()
  const query = searchParams.get("query") || ""
  return (
    <Typography variant="h4" gutterBottom>
      Search Results for {query}
      More to come!
    </Typography>
  )
}
