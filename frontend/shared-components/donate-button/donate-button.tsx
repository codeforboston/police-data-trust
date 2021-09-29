import React from "react"
import styles from "./donate-button.module.css"
import classnames from "classnames"

export interface Props extends React.HTMLProps<HTMLButtonElement> {
  loading?: boolean
}
export default function DonateButton({ className, loading, children, ...rest }: Props) {
  return (
    <button {...rest} className={classnames(styles.DonateButton, className)} type="submit">
      {loading ? <Spinner /> : children}
    </button>
  )
}

const Spinner = () => (
  <svg className={styles.spinner} viewBox="0 0 50 50">
    <circle className={styles.path} cx="25" cy="25" r="20" fill="none" strokeWidth="5"></circle>
  </svg>
)
