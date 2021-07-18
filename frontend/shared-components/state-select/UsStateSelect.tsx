import styles from "./state.module.css"
const states = [
  "AL",
  "AK",
  "AR",
  "AZ",
  "CA",
  "CO",
  "CT",
  "DC",
  "DE",
  "FL",
  "GA",
  "HI",
  "IA",
  "ID",
  "IL",
  "IN",
  "KS",
  "KY",
  "LA",
  "MA",
  "MD",
  "ME",
  "MI",
  "MN",
  "MO",
  "MS",
  "MT",
  "NC",
  "NE",
  "NH",
  "NJ",
  "NM",
  "NV",
  "NY",
  "ND",
  "OH",
  "OK",
  "OR",
  "PA",
  "RI",
  "SC",
  "SD",
  "TN",
  "TX",
  "UT",
  "VT",
  "VA",
  "WA",
  "WI",
  "WV",
  "WY",
]

export function USStateSelect() {
  return (
    <select className={styles.select}>
      {states.map((state) => (
        <option key={state} value={state}>
          {state}
        </option>
      ))}
    </select>
  )
}