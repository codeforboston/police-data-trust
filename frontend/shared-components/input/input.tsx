import * as React from "react"
import classNames from "classnames"
import styles from "./input.module.css"

/**
 * `<input>` tag with default stylings.
 * @param {React.InputHTMLAttributes<HTMLInputElement>} props - extends `HTMLInputElement` properties
 */
const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type, ...props }, ref) => {
    const { input } = styles
    return <input type={type} className={classNames(input, className)} ref={ref} {...props} />
  }
)
Input.displayName = "Input"

export default Input
