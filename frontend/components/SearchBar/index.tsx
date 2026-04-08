"use client"

import { TextField, InputAdornment, CircularProgress, Box } from "@mui/material"
import { Search } from "@mui/icons-material"
import { useSearch } from "@/providers/SearchProvider"
import React from "react"

export const SearchBar = () => {
  const {
    loading,
    setTerm,
    state: { term }
  } = useSearch()
  const [localInput, setLocalInput] = React.useState(term)

  React.useEffect(() => {
    setLocalInput(term)
  }, [term])

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 2,
        width: "100%"
      }}
    >
      <TextField
        variant="outlined"
        value={localInput}
        onChange={(e) => setLocalInput(e.target.value)}
        onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
          if (e.key === "Enter") {
            setTerm(localInput)
          }
        }}
        sx={{
          maxWidth: "546px",
          width: "100%",
          "& fieldset": { borderRadius: "20px" },
          "& .MuiInputBase-input": {
            overflow: "hidden",
            textOverflow: "ellipsis"
          }
        }}
        placeholder="Search officer, unit, or agency"
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            )
          }
        }}
      />
      {loading && (
        <CircularProgress
          size={24}
          aria-label="search loading indicator"
          data-testid="search-loading-spinner"
        />
      )}
    </Box>
  )
}

export default SearchBar
