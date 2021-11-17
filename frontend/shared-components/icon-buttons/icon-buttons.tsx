import { faGreaterThan, faPlusCircle } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React from "react"
import styles from "./icon-buttons.module.css"

export const GreaterThanButton = (props: { title?: string; onclick?: () => void }) => {
  return (
    <FontAwesomeIcon
      className={styles.actionBtn}
      title={props.title || "Greater Than"}
      icon={faGreaterThan}
      onClick={props.onclick}
    />
  )
}

export const CirclePlusButton = (props: { title?: string; onclick?: () => void }) => {
  return (
    <FontAwesomeIcon
      className={styles.actionBtn}
      title={props.title || "Plus"}
      icon={faPlusCircle}
      onClick={props.onclick}
    />
  )
}
