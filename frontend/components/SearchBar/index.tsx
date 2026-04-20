"use client"

import { TextField, InputAdornment, CircularProgress, Box } from "@mui/material"
import { Search } from "@mui/icons-material"
import { useSearch } from "@/providers/SearchProvider"
import { useAuth } from "@/providers/AuthProvider"
import React from "react"

type SearchBarProps = {
  showLoginRequiredMessage?: boolean
}

export const SearchBar = ({ showLoginRequiredMessage = false }: SearchBarProps) => {
  const {
    loading,
    setTerm,
    state: { term }
  } = useSearch()
  const { accessToken, hasHydrated } = useAuth()
  const [localInput, setLocalInput] = React.useState(term)
  const [showAuthError, setShowAuthError] = React.useState(false)

  React.useEffect(() => {
    setLocalInput(term)
  }, [term])

  React.useEffect(() => {
    if (accessToken) {
      setShowAuthError(false)
    }
  }, [accessToken])

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
      <Box sx={{ width: "100%", maxWidth: "546px" }}>
        <TextField
          variant="outlined"
          value={localInput}
          onChange={(e) => {
            setLocalInput(e.target.value)
            if (showAuthError) {
              setShowAuthError(false)
            }
          }}
          onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
            if (e.key === "Enter") {
              if (showLoginRequiredMessage && hasHydrated && !accessToken) {
                setShowAuthError(true)
                window.dispatchEvent(new Event("npdc:login-required-search"))
                return
              }

              setTerm(localInput)
            }
          }}
          error={showAuthError}
          helperText={showAuthError ? "Please log in before searching." : " "}
          sx={{
            width: "100%",
            "& fieldset": { borderRadius: "20px" },
            "& .MuiInputBase-input": {
              overflow: "hidden",
              textOverflow: "ellipsis"
            },
            "& .MuiFormHelperText-root": {
              marginLeft: 0,
              marginRight: 0
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
      </Box>
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
