"use client"

import React from "react"
import Link from "next/link"
import { Card, CardActionArea, Box } from "@mui/material"

type ResultCardShellProps = {
  href: string
  children: React.ReactNode
  isFirst?: boolean
  isLast?: boolean
  outlined?: boolean
}

export default function ResultCardShell({
  href,
  children,
  isFirst = false,
  isLast = false,
  outlined = true
}: ResultCardShellProps) {
  return (
    <Card
      variant={outlined ? "outlined" : undefined}
      elevation={0}
      sx={{
        border: outlined ? undefined : "none",
        boxShadow: "none",
        borderBottomLeftRadius: isLast ? "4px" : 0,
        borderBottomRightRadius: isLast ? "4px" : 0,
        borderTopLeftRadius: isFirst ? "4px" : 0,
        borderTopRightRadius: isFirst ? "4px" : 0,
        borderBottom: outlined && !isLast ? "none" : undefined
      }}
    >
      <CardActionArea
        component={Link}
        href={href}
        sx={{
          display: "block",
          textAlign: "left",
          "&:hover": {
            backgroundColor: "#f8f8f8"
          }
        }}
      >
        <Box sx={{ px: 6, py: 4 }}>{children}</Box>
      </CardActionArea>
    </Card>
  )
}