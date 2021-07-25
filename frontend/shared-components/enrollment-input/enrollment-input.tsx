import React, { FormEvent, useState } from 'react'
import styles from './enrollment-input.module.css'
import { FormLevelError } from '../index'
import { getTitleCaseFromCamel } from '../../helpers/syntax-helper'
import { EnrollmentInputNames, enrollmentValidation } from '../../models' 

interface EnrollmentInputProps{inputName: EnrollmentInputNames, isSubmitted: boolean, isShown?: boolean, size?: string}

export default function EnrollmentInput({ inputName, isSubmitted, isShown, size }: EnrollmentInputProps) {
  const { inputContainer, inputField } = styles
  const { errorMessage, pattern, inputType } = enrollmentValidation[inputName]

  const [inputId, errorId] = [`${inputName}Input`, `${inputName}Error`]
  const labelText: string = `${getTitleCaseFromCamel(inputName)}:`
  const displayType: string = isShown ? 'text' : inputType
  
  const ifNumber = (value: number): number | null => { return displayType === 'number' ? value : null }
  const checkIsValid = (value: string): boolean => { return !isSubmitted || pattern.test(value) }

  const [inputValue, setInputValue] = useState('')
  const [isValid, setIsValid] = useState(checkIsValid(''))

  function handleChange({ target: { value } }: FormEvent<HTMLInputElement>): void {
    value = value.toString()
    setInputValue(value)
    setIsValid(checkIsValid(value))
  }

  return (
    <div className={`defaultInputContainer ${inputContainer} ${!isValid && 'hasError'}`}>
      <label htmlFor={inputId}>{labelText}</label>
      <input 
        id={inputId} 
        className={`${inputField} ${styles[size]}`}
        max={ifNumber(99999)}
        min={ifNumber(0)}
        name={inputName}
        type={displayType}
        value={inputValue}
        aria-required="true" 
        aria-describedby={errorId}
        onChange={handleChange}
      />
      {!isValid && <FormLevelError errorId={errorId} errorMessage={errorMessage}/>}
    </div>
  )
}
