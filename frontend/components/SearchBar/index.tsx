"use client"

import { TextField, InputAdornment } from "@mui/material"
import { Search } from "@mui/icons-material"
import { useSearch } from "@/providers/SearchProvider"
import { useRouter } from "next/navigation"

export const SearchBar = () => {
  const { searchIncidents } = useSearch()

  const router = useRouter()

  const handleSearch = async (query: string) => {
    try {
      const results = await searchIncidents({ description: query })
      console.log("Search results:", results)
      // Navigate to the search results page with query parameters
      router.push(`/search?query=${encodeURIComponent(query)}`)
    } catch (error) {
      console.error("Search error:", error)
      // Handle error (e.g., show a notification)
      router.push(`/search?query=${encodeURIComponent(query)}`)
    }
  }

  return (
    <TextField
      label="Search"
      variant="outlined"
      onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") handleSearch((e.target as HTMLInputElement).value)
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
      placeholder="search incident, officer, id, department or try anything"
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
  )
}

export default SearchBar
