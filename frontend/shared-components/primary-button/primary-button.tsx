import React from "react"
import styles from "./primary-button.module.css"
import classnames from "classnames"

export interface Props extends React.HTMLProps<HTMLButtonElement> {
  loading?: boolean
}
function BaseButton({ className, loading, children, ...rest }: Props) {
  return (
    <button {...rest} className={classnames(className, styles.baseButton)}>
      {loading ? <Spinner /> : children}
    </button>
  )
}
export default function PrimaryButton({ className, loading, children, ...rest }: Props) {
  return(
    <BaseButton className={classnames(styles.primaryButton, className)} loading={loading} children={children} {...rest} />
    )
}

//a button disguised as a link
export function LinkButton({ className, loading, children, ...rest }: Props) {
  return(
   <BaseButton className={classnames(styles.linkButton, className)} loading={loading} children={children} {...rest} />
    )
}

const Spinner = () => (
  <svg className={styles.spinner} viewBox="0 0 50 50">
    <circle className={styles.path} cx="25" cy="25" r="20" fill="none" strokeWidth="5"></circle>
  </svg>
)
