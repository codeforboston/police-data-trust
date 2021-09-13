import React from "react"
import { useFormContext } from "react-hook-form"
import { FormLevelError } from ".."
import { getTitleCaseFromCamel } from "../../helpers"
import { PrimaryInputNames, primaryInputValidation } from "../../models"
import styles from "./primary-input.module.css"

interface PrimaryInputProps {
  inputName: PrimaryInputNames
  isShown?: boolean
  size?: string
}

export default function PrimaryInput({ inputName, isShown, size }: PrimaryInputProps) {
  const {
    register,
    formState: { errors }
  } = useFormContext()
  const { inputContainer, inputField } = styles
  const {
    errorMessage: defaultErrorMessage,
    pattern,
    inputType
  } = primaryInputValidation[inputName]

  const [inputId, errorId] = [`${inputName}Input`, `${inputName}Error`]
  const labelText: string = `${getTitleCaseFromCamel(inputName)}:`
  const displayType: string = isShown ? "text" : inputType
  const isValid = !errors[inputName]

  return (
    <div className={`defaultInputContainer ${inputContainer} ${!isValid && "hasError"}`}>
      <label htmlFor={inputId}>{labelText}</label>
      <input
        id={inputId}
        className={`${inputField} ${styles[size]}`}
        name={inputName}
        type={displayType}
        aria-required="true"
        aria-describedby={errorId}
        aria-invalid={!isValid}
        {...register(inputName, { required: true, pattern })}
      />
      {!isValid && (
        <FormLevelError
          errorId={errorId}
          errorMessage={errors[inputName].message || defaultErrorMessage}
        />
      )}
    </div>
  )
}
