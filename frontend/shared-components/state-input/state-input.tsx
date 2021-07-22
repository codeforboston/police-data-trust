import React, { FormEvent, useEffect, useState } from "react"
import styles from "./state-select.module.css"
import { FormLevelError } from '../index'
import { capitalizeFirstChar } from '../../helpers/syntax-helper'
import { states } from '../../models'

interface USAStateInputProps {
  isSubmitted: boolean
}
export default function USAStateInput({ isSubmitted }: USAStateInputProps) {
  const {stateSelect, hasError} = styles
  const [inputId, listId, errorId] = ['stateSelectInput', 'stateSelectList', 'stateSelectError']

  const [inputValue, setInputValue] = useState('')
  const [isValid, setIsValid] = useState(!isSubmitted)

  function checkIsValid(value: string): boolean {
    const matchingState = states.filter(({initials, name}) => {
      return value.toUpperCase() === initials || capitalizeFirstChar(value) === name
    })
    return !!matchingState.length
  }

  function handleInputChange({ target: { value } }: FormEvent<HTMLInputElement>): void {
    if (isSubmitted) setIsValid(checkIsValid(value))
    setInputValue(value)
  }

  useEffect(() => { if (isSubmitted) setIsValid(checkIsValid(inputValue)) }, [isSubmitted])
  
  return (
    <div className={`defaultInputContainer ${!isValid && 'hasError'}`}>
      <label htmlFor={inputId}>State:</label>
      <input 
        id={inputId}
        className={`${stateSelect} ${!isValid && hasError}`}
        list={listId}
        name={inputId}
        type="text"
        aria-required="true"
        onChange={handleInputChange}
      ></input>
      <datalist id={listId}>
        {states.map(({ initials, name }) => (
          <option key={initials} value={initials}>
            {name}
          </option>
        ))}
      </datalist>
      {!isValid && <FormLevelError errorId={errorId} errorMessage="Invalid"/>}
    </div>
  )
}      
