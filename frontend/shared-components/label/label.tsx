import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import classNames from "classnames"
import styles from "./label.module.css"

/**
 * Base `<label>` component that adds default stylings and accessibility features.
 * Extends Radix UI's `Label` component.
 * @param {LabelPrimitive.LabelProps} props - extends Radix UI's `Label` component
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/label#root}
 */
const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>
>(function LabelComponent({ className, ...props }, ref) {
  const { labelStyles } = styles
  return <LabelPrimitive.Root ref={ref} className={classNames(labelStyles, className)} {...props} />
})
Label.displayName = LabelPrimitive.Root.displayName

export default Label
