import { Box } from "@mui/material"

type StickySidebarLayoutProps = {
  main: React.ReactNode
  sidebar: React.ReactNode
  mainMaxWidth?: string | number
  sidebarWidth?: string | number
  stickyTop?: string | number
}

export default function StickySidebarLayout({
  main,
  sidebar,
  mainMaxWidth = "840px",
  sidebarWidth = "294px",
  stickyTop = "20px"
}: StickySidebarLayoutProps) {
  return (
    <Box sx={{ display: "flex", gap: 4, alignItems: "flex-start", flexWrap: "wrap" }}>
      <Box sx={{ flex: "1 1 700px", minWidth: 0, maxWidth: mainMaxWidth }}>{main}</Box>
      <Box
        sx={{
          flex: `0 0 ${sidebarWidth}`,
          width: "100%",
          maxWidth: sidebarWidth,
          position: "sticky",
          top: stickyTop,
          alignSelf: "flex-start",
          border: "1px solid #b3b3b3",
          borderRadius: "16px",
          padding: "16px",
          height: "fit-content",
          display: { xs: "none", md: "block" }
        }}
      >
        {sidebar}
      </Box>
    </Box>
  )
}
