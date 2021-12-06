import { useCallback, useEffect, useRef, useState } from "react"
import { Coord } from "../utilities/chartTypes"
import styles from "./popUps.module.css"

export interface PopUpProps {
  shouldShowPopUp?: boolean
  headerText?: string
  bodyText?: string
  location?: Coord
}

export default function PopUp(props: PopUpProps) {
  const { shouldShowPopUp, headerText, bodyText, location } = props

  const classNames = `${styles.popUp} ${shouldShowPopUp ? styles.popUpOpen : styles.popUpClosed}`

  const style = {
    transform: `translate(${location?.x}px, ${location?.y}px) translateX(50%)`
  }

  return (
    <div id={"popup"} className={classNames} style={style}>
      <header id="head" className={styles.popUpHead}>
        {headerText}
      </header>
      <div id="body" className={styles.popUpBody}>
        {bodyText}
      </div>
    </div>
  )
}
