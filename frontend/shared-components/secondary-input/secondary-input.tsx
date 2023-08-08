import classNames from "classnames"
import React from "react"
import { useFormContext } from "react-hook-form"
import { FormLevelError } from ".."
import { getTitleCaseFromCamel } from "../../helpers"
import { SecondaryInputNames, TooltipTypes } from "../../models"
import InfoTooltip, { InfoTooltipProps } from "../info-tooltip/info-tooltip"
import styles from "./secondary-input.module.css"

interface SecondaryInputProps {
  inputName: SecondaryInputNames
  isShown?: boolean
  size?: string
  defaultValue?: string
  className?: string
  tooltipProps?: InfoTooltipProps
  isRequired?: boolean
}

export default function SecondaryInput({
  inputName,
  tooltipProps
}: SecondaryInputProps) {
  const {
    register,
    formState: { errors }
  } = useFormContext()

  const [inputId, errorId] = [`${inputName}Input`, `${inputName}Error`]
  const labelText: string = `Date Source`
  const isValid = !errors[inputName]
  return (
    <div>
      <label htmlFor='source'>
        {labelText}
        {tooltipProps?.type && (
          <InfoTooltip
            type={tooltipProps?.type}
            icon={tooltipProps?.icon}
            iconSize={tooltipProps?.iconSize}
          />
        )}
      </label>
      <select name="source" id="source">
        <option value="mpv">MPV</option>
        <option value="cpdp">CPDP</option>
      </select>
    </div>
  )
}
