import styles from './application-response.module.css'

export default function ApplicationResponse({ isValid = false }) {
  const [textareaId, counterId, errorId] = ['applicationResponse', 'responseCounter', 'responseError']
  const charMax: number = 500
  const errorMessageText: string = `Please provide a response of at least ${charMax} characters`
  
  return (
    <div className={styles.responseContainer}>
      <label htmlFor={textareaId}>
        Why are you signing up to the NPDC?:
      </label>
      <textarea
        id={textareaId}
        maxLength={charMax}
        cols={33}
        rows={7}
        aria-required="true"
        aria-describedby={`${counterId} ${errorId}`}
      />
      <div className={styles.responseSubtext}>
        {!isValid && <p id={errorId}>ICON&nbsp;{errorMessageText}</p>}
        <p id={counterId}>XX/{charMax}</p>
      </div>
    </div>
  )
}
