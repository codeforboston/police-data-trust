import { faArrowDown, faArrowUp, faCheck } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import * as RadixSelect from "@radix-ui/react-select"
import classNames from "classnames"
import * as React from "react"
import styles from "./select.module.css"

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#root}
 */
const Root = RadixSelect.Root

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#group}
 */
const Group = RadixSelect.Group

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#value}
 */
const Value = RadixSelect.Value

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#trigger}
 */
const Trigger = React.forwardRef<
  React.ElementRef<typeof RadixSelect.Trigger>,
  React.ComponentPropsWithoutRef<typeof RadixSelect.Trigger>
>(({ className, children, ...props }, ref) => (
  <RadixSelect.Trigger ref={ref} className={classNames(styles.trigger, className)} {...props}>
    {children}
    <RadixSelect.Icon asChild>
      <FontAwesomeIcon icon={faArrowDown} />
    </RadixSelect.Icon>
  </RadixSelect.Trigger>
))
Trigger.displayName = RadixSelect.Trigger.displayName

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#scrollupbutton}
 */
const ScrollUpButton = React.forwardRef<
  React.ElementRef<typeof RadixSelect.ScrollUpButton>,
  React.ComponentPropsWithoutRef<typeof RadixSelect.ScrollUpButton>
>(({ className, ...props }, ref) => (
  <RadixSelect.ScrollUpButton
    ref={ref}
    className={classNames(styles.scrollBtn, className)}
    {...props}>
    <FontAwesomeIcon icon={faArrowUp} />
  </RadixSelect.ScrollUpButton>
))
ScrollUpButton.displayName = RadixSelect.ScrollUpButton.displayName

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#scrolldownbutton}
 */
const ScrollDownButton = React.forwardRef<
  React.ElementRef<typeof RadixSelect.ScrollDownButton>,
  React.ComponentPropsWithoutRef<typeof RadixSelect.ScrollDownButton>
>(({ className, ...props }, ref) => (
  <RadixSelect.ScrollDownButton
    ref={ref}
    className={classNames(styles.scrollBtn, className)}
    {...props}>
    <FontAwesomeIcon icon={faArrowDown} />
  </RadixSelect.ScrollDownButton>
))
ScrollDownButton.displayName = RadixSelect.ScrollDownButton.displayName

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#content}
 */
const Content = React.forwardRef<
  React.ElementRef<typeof RadixSelect.Content>,
  React.ComponentPropsWithoutRef<typeof RadixSelect.Content>
>(({ className, children, position = "popper", ...props }, ref) => (
  <RadixSelect.Portal>
    <RadixSelect.Content
      ref={ref}
      className={classNames(styles.content, position === "popper" && styles.popper, className)}
      position={position}
      {...props}>
      <ScrollUpButton />
      <RadixSelect.Viewport
        className={classNames(styles.contentViewport, position === "popper" && styles.popper)}>
        {children}
      </RadixSelect.Viewport>
      <ScrollDownButton />
    </RadixSelect.Content>
  </RadixSelect.Portal>
))
Content.displayName = RadixSelect.Content.displayName

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#label}
 */
const Label = React.forwardRef<
  React.ElementRef<typeof RadixSelect.Label>,
  React.ComponentPropsWithoutRef<typeof RadixSelect.Label>
>(({ className, ...props }, ref) => (
  <RadixSelect.Label ref={ref} className={classNames(styles.label, className)} {...props} />
))
Label.displayName = RadixSelect.Label.displayName

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#item}
 */
const Item = React.forwardRef<
  React.ElementRef<typeof RadixSelect.Item>,
  React.ComponentPropsWithoutRef<typeof RadixSelect.Item>
>(({ className, children, ...props }, ref) => (
  <RadixSelect.Item ref={ref} className={classNames(styles.item, className)} {...props}>
    <span className={styles.itemIndicator}>
      <RadixSelect.ItemIndicator>
        <FontAwesomeIcon icon={faCheck} />
      </RadixSelect.ItemIndicator>
    </span>

    <RadixSelect.ItemText>{children}</RadixSelect.ItemText>
  </RadixSelect.Item>
))
Item.displayName = RadixSelect.Item.displayName

/**
 * @see Documentation: {@link https://www.radix-ui.com/primitives/docs/components/select#separator}
 */
const Separator = React.forwardRef<
  React.ElementRef<typeof RadixSelect.Separator>,
  React.ComponentPropsWithoutRef<typeof RadixSelect.Separator>
>(({ className, ...props }, ref) => (
  <RadixSelect.Separator ref={ref} className={classNames(styles.separator, className)} {...props} />
))
Separator.displayName = RadixSelect.Separator.displayName

export {
  Content,
  Group,
  Item,
  Label,
  Root,
  ScrollDownButton,
  ScrollUpButton,
  Separator,
  Trigger,
  Value
}
