"use client"
import { TextField, InputAdornment } from "@mui/material"
import { Search } from "@mui/icons-material"

export const SearchBar = () => {
  return (
    <TextField
        label="Search"
        variant="outlined"
        sx={{
          "& fieldset": { borderRadius: "20px" },
          "maxWidth": "546px",
          "width": "100%",
        }}
        placeholder="search incident, officer, id, department or try anything"
        slotProps={{
          input: {
            sx: { borderRadius: "8px" },
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          },
        }}
      />
  )
}

export default SearchBar