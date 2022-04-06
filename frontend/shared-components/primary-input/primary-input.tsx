import classNames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { FormLevelError } from ".."
import { getTitleCaseFromCamel } from "../../helpers"
import { PrimaryInputNames, primaryInputValidation, TooltipTypes } from "../../models"
import InfoTooltip, { InfoTooltipProps } from "../info-tooltip/info-tooltip"
import styles from "./primary-input.module.css"

interface PrimaryInputProps {
  inputName: PrimaryInputNames
  isShown?: boolean
  size?: string
  defaultValue?: string
  className?: string
  tooltipProps?: InfoTooltipProps
  isRequired?: boolean
}

export default function PrimaryInput({
  inputName,
  isShown,
  size,
  defaultValue,
  className,
  tooltipProps,
  isRequired = true
}: PrimaryInputProps) {
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
    <div
      className={classNames(
        className,
        "defaultInputContainer",
        inputContainer,
        styles[size],
        !isValid && "hasError"
      )}>
      <label htmlFor={inputId}>
        {labelText}
        {tooltipProps?.type && (
          <InfoTooltip
            type={tooltipProps?.type}
            icon={tooltipProps?.icon}
            iconSize={tooltipProps?.iconSize}
          />
        )}
      </label>
      <input
        id={inputId}
        className={inputField}
        name={inputName}
        type={displayType}
        aria-required="true"
        aria-describedby={!isValid ? errorId : undefined}
        aria-invalid={!isValid}
        defaultValue={defaultValue}
        {...register(inputName, { required: isRequired, pattern })}
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
