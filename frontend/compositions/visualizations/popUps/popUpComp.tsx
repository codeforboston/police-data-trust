import { useCallback, useEffect, useRef, useState } from "react"
import { getTitleCaseFromCamel } from "../../../helpers"
import { Coord } from "../utilities/chartTypes"
import styles from "./popUps.module.css"

export interface PopUpProps {
  shouldShowPopUp?: boolean
  headerText?: string
  bodyText?: string
  location?: Coord
}

export default function PopUp({ shouldShowPopUp, headerText, bodyText, location }: PopUpProps) {
  const classNames = `${styles.popUp} ${shouldShowPopUp ? styles.popUpOpen : styles.popUpClosed}`

  const ariaLabel: string = `Detailed information about ${headerText}`
  const popUpBodyId: string = `${headerText}Details`

  const style = {
    transform: `translate(${location?.x}px, ${location?.y}px) translateX(50%)`
  }

  return (
    <div
      id={"popup"}
      className={classNames}
      style={style}
      aria-label={ariaLabel}
      aria-describedby={popUpBodyId}
      role="tooltip">
      <p id="head" className={styles.popUpHead}>
        {headerText}
      </p>
      <div id="body" className={styles.popUpBody}>
        {bodyText}
      </div>
    </div>
  )
}
