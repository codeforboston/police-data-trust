import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import PrimaryButton from "../primary-button/primary-button"
import styles from "./error-alert-dialog.module.css"
import { faExclamationTriangle } from "@fortawesome/free-solid-svg-icons"
import { SearchResultsTypes, alertContent } from "../../models"

interface ErrorAlertDialogProps {
  setError: Function
  searchResultType: SearchResultsTypes
}

export default function ErrorAlertDialog(props: ErrorAlertDialogProps) {
  const { errorAlertDialogContainer, innerErrorAlertDialogContainer, errorAlertDescription } =
    styles
  const { searchResultType } = props
  return (
    <div className={errorAlertDialogContainer}>
      <div className={innerErrorAlertDialogContainer}>
        <FontAwesomeIcon icon={faExclamationTriangle} size={"lg"} color={"red"} />
        <div className={errorAlertDescription}>
          <p>{alertContent[searchResultType]}</p>
          <p>Please revise search or explore map</p>
        </div>
      </div>
      <PrimaryButton type="submit" onClick={() => props.setError(false)}>
        Return
      </PrimaryButton>
    </div>
  )
}
