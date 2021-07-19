import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faExclamationCircle } from '@fortawesome/free-solid-svg-icons'
import React, { FormEvent, useState } from 'react'
import styles from './enrollment-input.module.css'
import { getTitleCaseFromCamel } from '../../helpers/syntax-helper'
import { EnrollmentInputNames, inputValidation } from '../../models' 

interface EnrollmentInputProps { inputName: EnrollmentInputNames, isSubmitted: boolean, isPasswordShown?: boolean  }

export default function EnrollmentInput({ inputName, isSubmitted, isPasswordShown }: EnrollmentInputProps) {
  const { inputContainer, inputField, inputError, errorMessage } = styles
  const { errorMessageText, pattern, inputType } = inputValidation[inputName]

  const [inputId, errorId] = [`${inputName}Input`, `${inputName}Error`]
  const labelText: string = `${getTitleCaseFromCamel(inputName)}:`
  const displayType: string = isPasswordShown ? 'text' : inputType

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
        aria-required="true" 
        aria-describedby={errorId}
        className={`${inputField} ${!isValid && inputError}`} 
        name={inputName}
        type={displayType}
        value={inputValue}
        onChange={handleChange}
      />
      {!isValid && 
      <p id={errorId} className={errorMessage}>
        <FontAwesomeIcon aria-hidden="true" icon={faExclamationCircle}/>
        &nbsp;{errorMessageText}
      </p>}
    </div>
  )
}

