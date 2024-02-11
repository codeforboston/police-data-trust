import React from "react"
import styles from "./primary-button.module.css"
import classnames from "classnames"

export interface Props extends React.HTMLProps<HTMLButtonElement> {
  loading?: boolean
  type?: "button" | "submit" | "reset"
}

const Button = React.forwardRef<HTMLButtonElement, Props>(function PrimaryButton(
  { className, loading, type, children, ...rest }: Props,
  ref
) {
  return (
    <button
      ref={ref}
      type={type || "submit"}
      className={classnames(styles.primaryButton, className)}
      {...rest}>
      {loading ? <Spinner /> : children}
    </button>
  )
})

const Spinner = () => (
  <svg className={styles.spinner} viewBox="0 0 50 50">
    <circle className={styles.path} cx="25" cy="25" r="20" fill="none" strokeWidth="5"></circle>
  </svg>
)

export default Button
