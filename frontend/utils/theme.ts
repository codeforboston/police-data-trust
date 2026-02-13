"use client"

import { createTheme } from "@mui/material/styles"

const theme = createTheme({
  palette: {
    primary: { main: "#2196F3" },
    secondary: { main: "#303463" },
    text: { primary: "#000000", secondary: "#344054" }
  },
  typography: {
    fontFamily: "Inter, Roboto, Helvetica, Arial, sans-serif"
  }
})

export default theme
