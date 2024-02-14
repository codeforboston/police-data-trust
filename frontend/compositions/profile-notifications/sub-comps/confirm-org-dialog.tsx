import classNames from "classnames"
import { PrimaryButton, Dialog as D } from "../../../shared-components"
import styles from "./confirm-org-dialog.module.css"
import { useState } from "react"

interface ConfirmOrgDialogProps {
  organizationName: string
}

export default function ConfirmOrgDialog({ organizationName }: ConfirmOrgDialogProps) {
  const [open, setOpen] = useState(false)
  // TODO: determine if user is joining or leaving

  const handleConfirm = () => {
    // TODO: Join/Leave organization
    console.log("Joined or Left Organization: ", organizationName)
    setOpen(false)
  }

  const handleNotYet = () => {
    setOpen(false)
  }

  return (
    <D.Root open={open} onOpenChange={setOpen}>
      <D.Trigger asChild>
        <PrimaryButton className={styles.actionBtn}>Join</PrimaryButton>
      </D.Trigger>
      <D.Content>
        <D.Header>
          <D.Title>Are you sure you want to join {organizationName}?</D.Title>
        </D.Header>
        <D.Footer className={styles.btnContainer}>
          <PrimaryButton
            className={classNames(styles.btn, styles.confirmBtn)}
            onClick={handleConfirm}>
            Join
          </PrimaryButton>
          <PrimaryButton
            className={classNames(styles.btn, styles.notYetBtn)}
            onClick={handleNotYet}>
            Not Yet
          </PrimaryButton>
        </D.Footer>
      </D.Content>
    </D.Root>
  )
}
