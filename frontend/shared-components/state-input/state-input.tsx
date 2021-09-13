import React from "react"
import { useFormContext } from "react-hook-form"
import { capitalizeFirstChar } from "../../helpers"
import { states } from "../../models"
import { FormLevelError } from "../index"
import styles from "./state-input.module.css"

export default function USAStateInput() {
  const {
    register,
    formState: { errors }
  } = useFormContext()
  const inputName = USAStateInput.inputName
  const { stateSelect, hasError } = styles
  const [inputId, listId, errorId] = ["stateSelectInput", "stateSelectList", "stateSelectError"]
  const isValid = !errors[inputName]

  return (
    <div className={`defaultInputContainer ${!isValid && "hasError"}`}>
      <label htmlFor={inputId}>State:</label>
      <input
        id={inputId}
        className={`${stateSelect} ${!isValid && hasError}`}
        list={listId}
        name={inputId}
        type="text"
        aria-required="true"
        {...register(inputName, { required: true, validate: validateState })}
      />
      <datalist id={listId}>
        {states.map(({ initials, name }) => (
          <option key={initials} value={initials}>
            {name}
          </option>
        ))}
      </datalist>
      {!isValid && (
        <FormLevelError errorId={errorId} errorMessage={errors[inputName].message || "Invalid"} />
      )}
    </div>
  )
}

USAStateInput.inputName = "state"

function validateState(value: string) {
  const valid = !!states.find(
    ({ initials, name }) => value.toUpperCase() === initials || capitalizeFirstChar(value) === name
  )
  if (!valid) {
    return "Please enter a state like IL or Illinois"
  }
}
