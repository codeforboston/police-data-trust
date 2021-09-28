import React, { MouseEvent, useState } from "react"
import styles from "./password-aid.module.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { passwordToggleViews } from "../../models"

interface PasswordAidProps {
  id: string
  onDisplayChange: Function
}

export default function PasswordAid({ id, onDisplayChange }: PasswordAidProps) {
  const { passwordAid, passwordToggle } = styles
  const { showView, hideView } = passwordToggleViews

  const [{ icon, isHidden, text }, setPasswordView] = useState(showView)

  function togglePasswordView($event: MouseEvent<HTMLButtonElement>): void {
    $event.preventDefault()
    const newView = isHidden ? hideView : showView

    onDisplayChange(!isHidden)
    setPasswordView(newView)
  }

  return (
    <div className={passwordAid}>
      <p id={id}>Use eight or more characters with a mix of letters, numbers, and symbols</p>
      <button
        className={passwordToggle}
        role="switch"
        aria-checked={isHidden}
        onClick={togglePasswordView}>
        <FontAwesomeIcon icon={icon} /> {text}
      </button>
    </div>
  )
}
