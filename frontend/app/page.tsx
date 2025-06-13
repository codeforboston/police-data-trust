"use client"
import styles from "./page.module.css"
import { TextField, InputAdornment } from "@mui/material"
import { Search } from "@mui/icons-material"

export default function Home() {
  return (
    <div className={styles.page}>
      <h1 className={styles.heading}>How can we help you?</h1>
      <TextField
        className={styles.input}
        label="Search"
        variant="outlined"
        sx={{
          "& fieldset": { borderRadius: "20px" }
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
      <LatestUpdates />
      <UpToDateNotification />
    </div>
  )
}

const LatestUpdates = () => {
  return (
    <section className={styles.latestUpdatesWrapper}>
      <h2 className={styles.latestUpdatesHeading}>Latest Updates</h2>
      <ul className={styles.cardSection}>
        <UpdateCard
          title="Incident"
          updates={[
            "New add one",
            "New add one",
            "New add one",
          ]}
        />
        <UpdateCard
          title="Post"
          updates={[
            "New add one",
            "New add one",
            "New add one",
          ]}
        />
        <UpdateCard
          title="Following"
          updates={[
            "New add one",
            "New add one",
            "New add one",
          ]}
        /> 
      </ul>
    </section>
  )
}

type UpdateCardProps = {
  title: string;
  updates: string[];
}

const UpdateCard = ({ title, updates }: UpdateCardProps) => {
  return (
    <div className={styles.card}>
      <h3 className={styles.cardTitle}>{title}</h3>
      <ul className={styles.updateList}>
        {updates.map((update, index) => (
          <li className={styles.cardItem} key={index}>{update}</li>
        ))}
      </ul>
    </div>
  )
}

const UpToDateNotification = () => {
  return (
    <div className={styles.upToDateNotification}>
      <div className={styles.upToDateIcon}/>
      <p>All the resources have been updated to the latest version/dates</p>
    </div>
  )
}
