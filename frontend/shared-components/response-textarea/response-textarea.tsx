import styles from "./response-textarea.module.css"
import { FormLevelError } from "../index"
import { ChangeEvent, useEffect, useState } from "react"
import { useFormContext } from "react-hook-form"

export default function ResponseTextArea() {
  const {
    register,
    formState: { errors }
  } = useFormContext()
  const [textareaId, counterId, errorId] = ["responseTextArea", "responseCounter", "responseError"]
  const [charMax, charMin] = [500, 150]
  const inputName = ResponseTextArea.inputName
  const defaultErrorMessage = `Please provide a response of at least ${charMin} characters`

  const [charCount, setCharCount] = useState(0)
  const isValid = !errors[inputName]

  const { onChange: formOnChange, ...inputAttributes } = register(inputName, {
    required: true,
    minLength: charMin,
    maxLength: charMax
  })
  const onChange = (e: any) => {
    setCharCount(e.target.value.length)
    formOnChange(e)
  }

  return (
    <div className={`defaultInputContainer ${!isValid && "hasError"}`}>
      <label htmlFor={textareaId}>Why are you signing up to the NPDC?:</label>
      <textarea
        className={styles.responseArea}
        id={textareaId}
        cols={52}
        rows={7}
        aria-required="true"
        aria-describedby={`${counterId} ${!isValid ? errorId : null}`}
        onChange={onChange}
        {...inputAttributes}
      />
      <div className={styles.responseSubtext}>
        <p id={counterId}>
          {charCount}/{charMax}
        </p>
        {!isValid && (
          <FormLevelError
            errorId={errorId}
            errorMessage={errors[inputName].message || defaultErrorMessage}
          />
        )}
      </div>
    </div>
  )
}

ResponseTextArea.inputName = "reponseText"
