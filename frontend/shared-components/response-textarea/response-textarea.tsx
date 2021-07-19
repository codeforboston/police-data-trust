import styles from './response-textarea.module.css'
import { FormLevelError } from '../index'
import { FormEvent, useState } from 'react'

interface ResponseTextAreaProps { isSubmitted: boolean}

export default function ResponseTextArea({ isSubmitted }: ResponseTextAreaProps) {
  const { responseContainer, responseError, responseSubtext} = styles
  const [textareaId, counterId, errorId] = ['ResponseTextArea', 'responseCounter', 'responseError']
  const [charMax, charMin] = [500, 150]

  const errorMessage: string = `Please provide a response of at least ${charMin} characters`
  
  const [charCount, setCharCount] = useState(0)
  const [isValid, setIsValid] = useState(!isSubmitted)

  function handleChange($event: FormEvent<HTMLTextAreaElement>): void {
    const currCharCount: number = $event.target.value.length

    if (isSubmitted) setIsValid(currCharCount >= charMin)
    setCharCount(currCharCount)
  }

  return (
    <div className={`${responseContainer} ${!isValid && responseError}`}>
      <label htmlFor={textareaId}>
        Why are you signing up to the NPDC?:
      </label>
      <textarea
        id={textareaId}
        cols={33}
        rows={7}
        maxLength={charMax}
        aria-required="true"
        aria-describedby={`${counterId} ${errorId}`}
        onChange={handleChange}
      />
      <div className={responseSubtext}>
        <p id={counterId}>{charCount}/{charMax}</p>
        {!isValid && <FormLevelError errorId={errorId} errorMessage={errorMessage} />}
      </div>
    </div>
  )
}
