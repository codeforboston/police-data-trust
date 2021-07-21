import React, { FormEvent, useState } from "react"
import styles from "./state-select.module.css"
import { FormLevelError } from '../index'
import { states } from '../../models'

interface USStateSelectProps { isSubmitted: boolean }
export default function USStateSelect({ isSubmitted }: USStateSelectProps) {
  const [selectId, errorId] = ['stateSelect', 'stateSelectError']

  const [isValid, setIsValid] = useState(!isSubmitted)

  function handleChange(event: React.ChangeEvent<HTMLInputElement>): void {
    // if (isSubmitted) setIsValid(event.target.value)
    console.log(event);
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
        {states.map(({ initials, name }) => (
          <option key={initials} value={initials} aria-label={name}>
            {initials}
          </option>
        ))}
      </select>
      {!isValid && <FormLevelError errorId={errorId} errorMessage="Required"/>}
    </div>
  )
}