import { Officer } from "@/utils/api"
import { Avatar, IconButton, Typography } from "@mui/material"
import styles from "./identityCard.module.css"
import { US_STATES } from "@/utils/constants"
import AddToPhotosOutlinedIcon from "@mui/icons-material/AddToPhotosOutlined"

function getAge(dob: string): number {
  const today = new Date()
  const age = today.getFullYear() - parseInt(dob)

  return age
}

function getStateName(abbreviation: string | undefined): string {
  if (!abbreviation) return ""
  const state = US_STATES.find((s) => s.abbreviation === abbreviation)
  return state ? state.name : abbreviation
}

// TODO: Add to collection button functionality and real image source
export default function IdentityCard(officer: Officer) {
  const currentEmployment = officer.employment_history?.find((emp) => !emp.latest_date)

  return (
    <div className={styles.identityCard}>
      <IconButton
        aria-label="add to collection"
        size="small"
        color="inherit"
        sx={{ position: "absolute", top: 16, right: 16 }}
      >
        <AddToPhotosOutlinedIcon sx={{ width: 16, height: 16 }} />
      </IconButton>
      <Avatar sx={{ width: 88, height: 88 }} src={"/broken-image.jpg"} />
      <div>
        <Typography variant="subtitle1" component="h1" fontWeight="bold">
          {officer.first_name}{" "}
          {officer.middle_name && officer.middle_name.length === 1
            ? `${officer.middle_name}.`
            : officer.middle_name}{" "}
          {officer.last_name}
        </Typography>
        <Typography variant="body2">
          {officer.ethnicity} {officer.gender?.toLowerCase()}
          {officer.year_of_birth && `, ${getAge(officer.year_of_birth)} years old`}
        </Typography>
        {currentEmployment && (
          <Typography variant="body2">
            {currentEmployment.highest_rank || "Officer"} at {currentEmployment.agency_name}
            {currentEmployment.state && `, ${getStateName(currentEmployment.state)}`}
          </Typography>
        )}
      </div>
    </div>
  )
}
