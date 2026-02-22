import TextField from "@mui/material/TextField/TextField"
import styles from "./filter.module.css"
import {
  Checkbox,
  InputAdornment,
  FormGroup,
  Box,
  FormControlLabel,
  Typography
} from "@mui/material"
import { Search } from "@mui/icons-material"
import { KeyboardEvent, useState, ChangeEvent } from "react"
import { useSearch } from "@/providers/SearchProvider"
import { useSearchParams } from "next/navigation"

const FILTER_GROUP_1 = [
  { id: 1, title: "All the locations", count: 56 },
  { id: 2, title: "New York City", count: 15 },
  { id: 3, title: "Texas State", count: 2 }
]
const FILTER_GROUP_2 = [
  { id: 1, title: "50.org", count: 10 },
  { id: 2, title: "Accountable", count: 5 },
  { id: 3, title: "CAPStat", count: 3 }
]

const Filter = () => {
  const [localLocationInputState, setLocalLocationInputState] = useState('')
  const { searchAll } = useSearch()
  const searchParams = useSearchParams()
  function changeLocalSearchVal(e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const changeVal = e.target.value
    // TODO: this is causing the other search box to refresh as wll
    setLocalLocationInputState(changeVal)
  }
  async function locationFilterSearch(e: KeyboardEvent<HTMLDivElement>) {
    if (e.key === 'Enter') {
      const currentQuery = searchParams.get('query') ?? ''
      await searchAll({ query: currentQuery, location: localLocationInputState })
    }

  }
  return (
    <section className={styles.filterWrapper}>
      <h3 className={styles.filterTitleText}>Filters</h3>
      <div className={styles.filterContentsWrapper}>
        <FilterGroup
          onChangeHandler={changeLocalSearchVal}
          searchHandler={locationFilterSearch}
          value={localLocationInputState}
          withSearch
          filters={FILTER_GROUP_1}
          title="Location"
        />
        <FilterGroup filters={FILTER_GROUP_2} title="Data Source" />
      </div>
    </section>
  )
}

type FilterGroupProps = {
  searchHandler?: (e: KeyboardEvent<HTMLDivElement>) => void
  withSearch?: boolean
  value?: string
  onChangeHandler?: (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void
  filters: FilterItem[]
  title: string
}

type FilterItem = {
  id: string | number
  title: string
  count: number
}

const FilterGroup = ({ withSearch = false, filters = [], title, searchHandler, value, onChangeHandler }: FilterGroupProps) => {
  return (
    <FormGroup sx={{ marginBottom: "1.5rem" }}>
      <Typography variant="subtitle1" sx={{ marginBlockEnd: "0.5rem", fontWeight: "600" }}>
        {title}
      </Typography>
      {(withSearch && searchHandler !== null) && (
        <TextField
          id="search"
          variant="outlined"
          fullWidth
          onKeyDown={searchHandler}
          onChange={onChangeHandler}
          value={value}
          sx={{
            marginBottom: "1rem",
            "& .MuiInputBase-root": {
              height: "40px"
            }
          }}
          placeholder="search city, state..."
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
      )}
      {filters.map((filter) => (
        <Box
          key={filter.id}
          sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}
        >
          <FormControlLabel control={<Checkbox />} label={filter.title} />
          <Typography variant="body2" color="text.secondary">
            {filter.count}
          </Typography>
        </Box>
      ))}
      <Typography variant="body2" color="text.secondary" className={styles.filterText}>
        Show More...
      </Typography>
    </FormGroup>
  )
}

export default Filter
