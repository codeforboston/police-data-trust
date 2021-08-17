import React, { ChangeEvent, useEffect, useState } from "react"
import styles from "./primary-input.module.css"
import { FormLevelError } from ".."
import { getTitleCaseFromCamel } from "../../helpers/syntax-helper"
import { PrimaryInputNames, primaryInputValidation } from "../../models"

interface PrimaryInputProps {
  inputName: PrimaryInputNames
  isSubmitted: boolean
  isShown?: boolean
  size?: string
}

export default function PrimaryInput({
  inputName,
  isSubmitted,
  isShown,
  size,
}: PrimaryInputProps) {
  const { inputContainer, inputField } = styles
  const { errorMessage, pattern, inputType } = primaryInputValidation[inputName]

  const [inputId, errorId] = [`${inputName}Input`, `${inputName}Error`]
  const labelText: string = `${getTitleCaseFromCamel(inputName)}:`
  const displayType: string = isShown ? "text" : inputType

  const ifNumber = (value: number): number | null => {
    return displayType === "number" ? value : null
  }
  const checkIsValid = (value: string): boolean => {
    return !isSubmitted || (value && pattern.test(value))
  }

  const [inputValue, setInputValue] = useState("")
  const [isValid, setIsValid] = useState(checkIsValid(""))

  function handleInputChange({ target: { value } }: ChangeEvent<HTMLInputElement>): void {
    value = value.toString()
    setInputValue(value)
    setIsValid(checkIsValid(value))
  }

  useEffect(() => { if (isSubmitted) setIsValid(checkIsValid(inputValue)) }, [isSubmitted])

  return (
    <div className={`defaultInputContainer ${inputContainer} ${!isValid && "hasError"}`}>
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
        onChange={handleInputChange}
      />
      {!isValid && <FormLevelError errorId={errorId} errorMessage={errorMessage} />}
    </div>
  )
}
