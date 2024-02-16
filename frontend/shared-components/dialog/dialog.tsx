import * as React from "react"
import * as RadixDialog from "@radix-ui/react-dialog"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faWindowClose } from "@fortawesome/free-solid-svg-icons"
import classNames from "classnames"
import styles from "./dialog.module.css"

/**
 * The base component for creating dialogs. Manages dialog state (open/closed) and contains all parts of a dialog.
 * @param {RadixDialog.DialogProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#root}
 */
const Root = RadixDialog.Root

/**
 * An interactive element that triggers the opening of the dialog.
 * @param {RadixDialog.DialogTriggerProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#trigger}
 */
const Trigger = RadixDialog.Trigger

/**
 * Creates a portal into `document.body` for the dialog overlay and content.
 * @param {RadixDialog.DialogPortalProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#portal}
 */
const Portal = RadixDialog.Portal

/**
 * Button for closing the dialog.
 * @param {RadixDialog.DialogCloseProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#close}
 */
const Close = RadixDialog.Close

/**
 * A semi-transparent overlay that covers the screen when the dialog is open.
 * Adds default styling and forwards an optional `ref`.
 * @param {RadixDialog.DialogOverlayProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#overlay}
 */
const Overlay = React.forwardRef<
  React.ElementRef<typeof RadixDialog.Overlay>,
  React.ComponentPropsWithoutRef<typeof RadixDialog.Overlay>
>(({ className, ...props }, ref) => {
  const { dialogOverlay } = styles
  return (
    <RadixDialog.Overlay ref={ref} className={classNames(dialogOverlay, className)} {...props} />
  )
})
Overlay.displayName = RadixDialog.Overlay.displayName

/**
 * The main content area of the dialog. Provides default styling, establishes the Portal, Overlay, and Close dialog components, and forwards an optional `ref`.
 * @param {RadixDialog.DialogContentProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#content}
 */
const Content = React.forwardRef<
  React.ElementRef<typeof RadixDialog.Content>,
  React.ComponentPropsWithoutRef<typeof RadixDialog.Content>
>(({ className, children, ...props }, ref) => {
  const { dialogContent, dialogClose } = styles
  return (
    <Portal>
      <Overlay />
      <RadixDialog.Content ref={ref} className={classNames(dialogContent, className)} {...props}>
        {children}
        <Close className={dialogClose}>
          <FontAwesomeIcon icon={faWindowClose} size="lg" />
          <span className="sr-only">Close</span>
        </Close>
      </RadixDialog.Content>
    </Portal>
  )
})
Content.displayName = RadixDialog.Content.displayName

/**
 * `div` container with default styling for the dialog's header content.
 */
const Header = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => {
  const { header } = styles
  return <div className={classNames(header, className)} {...props} />
}
Header.displayName = "Dialog.Header"

/**
 * `div` container with default styling for the dialog's footer content.
 */
const Footer = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => {
  const { footer } = styles
  return <div className={classNames(footer, className)} {...props} />
}
Footer.displayName = "Dialog.Footer"

/**
 * The dialog's title text.
 * Adds default styling and forwards an optional `ref`.
 * Fits nicely into the `Dialog.Header` component.
 * @param {RadixDialog.DialogTitleProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#title}
 */
const Title = React.forwardRef<
  React.ElementRef<typeof RadixDialog.Title>,
  React.ComponentPropsWithoutRef<typeof RadixDialog.Title>
>(({ className, ...props }, ref) => {
  const { title } = styles
  return <RadixDialog.Title ref={ref} className={classNames(title, className)} {...props} />
})
Title.displayName = RadixDialog.Title.displayName

/**
 * Descriptive text within the dialog.
 * Adds default styling and forwards an optional `ref`.
 * Fits nicely as a subheader in the `Dialog.Header` component.
 * @param {RadixDialog.DialogDescriptionProps} props - Documentation: {@link https://www.radix-ui.com/primitives/docs/components/dialog#description}
 */
const Description = React.forwardRef<
  React.ElementRef<typeof RadixDialog.Description>,
  React.ComponentPropsWithoutRef<typeof RadixDialog.Description>
>(({ className, ...props }, ref) => {
  const { description } = styles
  return (
    <RadixDialog.Description ref={ref} className={classNames(description, className)} {...props} />
  )
})
Description.displayName = RadixDialog.Description.displayName

export { Root, Portal, Overlay, Close, Trigger, Content, Header, Footer, Title, Description }
