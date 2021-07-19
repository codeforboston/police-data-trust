import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faExclamationCircle } from '@fortawesome/free-solid-svg-icons'
import React, { FormEvent, useState } from 'react'
import styles from './enrollment-input.module.css'
import { getTitleCaseFromCamel } from '../../helpers/syntax-helper'
import { EnrollmentInputNames, enrollmentValidation } from '../../models' 

interface EnrollmentInputProps{inputName: EnrollmentInputNames, isSubmitted: boolean, isShown?: boolean, size?: string}

export default function EnrollmentInput({ inputName, isSubmitted, isShown, size }: EnrollmentInputProps) {
  const { inputContainer, inputField, inputError, errorMessage } = styles
  const { errorMessageText, pattern, inputType } = enrollmentValidation[inputName]

  const [inputId, errorId] = [`${inputName}Input`, `${inputName}Error`]
  const labelText: string = `${getTitleCaseFromCamel(inputName)}:`
  const displayType: string = isShown ? 'text' : inputType
  
  const ifNumber = (value: number): number | null => { return displayType === 'number' ? value : null }
  const checkIsValid = (value: string): boolean => { return !isSubmitted || pattern.test(value) }

  const [inputValue, setInputValue] = useState('')
  const [isValid, setIsValid] = useState(checkIsValid(''))

  function handleChange({ target: { value } }: FormEvent<HTMLInputElement>): void {
    setInputValue(value)
    setIsValid(checkIsValid(value))
  }

  return (
    <div className={inputContainer}>
      <label htmlFor={inputId}>{labelText}</label>
      <input 
        id={inputId} 
        className={`${inputField} ${styles[size]} ${!isValid && inputError}`} 
        max={ifNumber(99999)}
        min={ifNumber(0)}
        name={inputName}
        type={displayType}
        value={inputValue}
        aria-required="true" 
        aria-describedby={errorId}
        onChange={handleChange}
      />
      {!isValid && 
        <p id={errorId} className={errorMessage}>
          <FontAwesomeIcon aria-hidden="true" icon={faExclamationCircle}/>
          &nbsp;{errorMessageText}
        </p>
      }
    </div>
  )
}


