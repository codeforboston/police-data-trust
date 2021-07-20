import React, { FormEvent, useState } from "react"
import styles from "./state-select.module.css"
import { FormLevelError } from '../index'

const states: string[] = [
  "AL", "AK", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", 
  "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "NE", "NH", "NJ", "NM", "NV", "NY", 
  "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WI", "WV", "WY"
]

interface USStateSelectProps { isSubmitted: boolean }
export default function USStateSelect({ isSubmitted }: USStateSelectProps) {
  const [selectId, errorId] = ['stateSelect', 'stateSelectError']

  const [isValid, setIsValid] = useState(!isSubmitted)

  function handleChange({ target: { value } }: FormEvent<HTMLSelectElement>): void {
    if (isSubmitted) setIsValid(!!value)
  }
  
  return (
    <div className={`defaultInputContainer ${!isValid && 'hasError'}`}>
      <label htmlFor={selectId}>State:</label>
      <select 
        id={selectId} 
        className={styles.stateSelect}
        name="states" 
        defaultValue=""
        aria-required="true" 
        aria-describedby={errorId} 
        onChange={handleChange}
      >
        <option disabled value="">&ndash; &ndash;</option>
        {states.map((state) => (
          <option key={state} value={state}>
            {state}
          </option>
        ))}
      </select>
      {!isValid && <FormLevelError errorId={errorId} errorMessage="Required"/>}
    </div>
  )
}