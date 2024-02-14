import * as LabelPrimitive from "@radix-ui/react-label"
import { Slot } from "@radix-ui/react-slot"
import classNames from "classnames"
import * as React from "react"
import {
  Controller,
  ControllerProps,
  FieldPath,
  FieldValues,
  FormProvider,
  UseFormReturn,
  useFormContext
} from "react-hook-form"
import useId from "../../helpers/hooks/useId"
import { Label as FormLabel } from "../../shared-components"
import styles from "./form.module.css"

type FormProps<T extends FieldValues> = {
  children: React.ReactNode
  formMethods: UseFormReturn<T>
} & React.FormHTMLAttributes<HTMLFormElement>

/**
 * Base component for creating forms.
 * Wraps children elements with `FormProvider` from "react-hook-form" and a base `form` element.
 * @param {React.ReactNode} children - any children components (form fields)
 * @param {UseFormReturn<T>} formMethods - returned the `useForm()` hook from "react-hook-form"
 * @param {React.FormHTMLAttributes<HTMLFormElement>} formProps - extends `HTMLFormElement` properties
 */
const Root = function <T extends FieldValues>({
  children,
  formMethods,
  ...formProps
}: FormProps<T>) {
  return (
    <FormProvider {...formMethods}>
      <form {...formProps}>{children}</form>
    </FormProvider>
  )
}
Root.displayName = "Form"

type FormFieldContextValue<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
> = {
  name: TName
}

const FormFieldContext = React.createContext<FormFieldContextValue>({} as FormFieldContextValue)

/**
 * Defines a field within a `Form` component.
 * Builds a controlled form field with `Controller` component from "react-hook-form".
 * Provides field name to child components via context.
 * @param {ControllerProps<TFieldValues, TName>} props - extends `Controller` props from "react-hook-form".  Documentation: {@link https://react-hook-form.com/docs/usecontroller/controller}
 */
const Field = <
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
>({
  ...props
}: ControllerProps<TFieldValues, TName>) => {
  return (
    <FormFieldContext.Provider value={{ name: props.name }}>
      <Controller {...props} />
    </FormFieldContext.Provider>
  )
}
Field.displayName = "FormField"

type FormItemContextValue = {
  id: string
}

const FormItemContext = React.createContext<FormItemContextValue>({} as FormItemContextValue)

/**
 * Wrapper around form elements for accessibility purposes.
 * Gives form elements an accessibility `id` via context.
 * @param {React.HTMLAttributes<HTMLDivElement>} props - extends `HTMLDivElement` properties
 */
const Item = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    const { formItem } = styles
    const id = useId()

    return (
      <FormItemContext.Provider value={{ id }}>
        <div ref={ref} className={classNames(formItem, className)} {...props} />
      </FormItemContext.Provider>
    )
  }
)
Item.displayName = "FormItem"

/**
 * Convenient hook used to get a form field's state with additional accessibility ID properties.
 * @returns {object} field state with additional `id` properties for accessibility.
 */
const useFormField = () => {
  const fieldContext = React.useContext(FormFieldContext)
  const itemContext = React.useContext(FormItemContext)
  const { getFieldState, formState } = useFormContext()

  const fieldState = getFieldState(fieldContext.name, formState)

  if (!fieldContext) {
    throw new Error("useFormField should be used within <Form.Field>")
  }

  const { id } = itemContext

  return {
    id,
    name: fieldContext.name,
    formItemId: `${id}-form-item`,
    formDescriptionId: `${id}-form-item-description`,
    formMessageId: `${id}-form-item-message`,
    ...fieldState
  }
}

/**
 * Creates `<label>` element for the given form field.
 * Adds default styling, and utilizes Radix UI for accessibility.
 * @param {LabelPrimitive.LabelProps} props - extends Radix UI's `Label` element and `HTMLLabelElement` properties
 */
const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>
>(({ className, ...props }, ref) => {
  const { textDestructive } = styles
  const { error, formItemId } = useFormField()

  return (
    <FormLabel
      ref={ref}
      className={classNames(error && textDestructive, className)}
      htmlFor={formItemId}
      {...props}
    />
  )
})
Label.displayName = "FormLabel"

/**
 * Directly wraps any form input component.
 * Gives child component accessibility properties.
 * @param {SlotProps & React.RefAttributes<HTMLElement>} props - extends `SlotProps` and `HTMLElement` properties
 */
const Control = React.forwardRef<
  React.ElementRef<typeof Slot>,
  React.ComponentPropsWithoutRef<typeof Slot>
>(({ ...props }, ref) => {
  const { error, formItemId, formDescriptionId, formMessageId } = useFormField()

  return (
    <Slot
      ref={ref}
      id={formItemId}
      aria-describedby={!error ? `${formDescriptionId}` : `${formDescriptionId} ${formMessageId}`}
      aria-invalid={!!error}
      {...props}
    />
  )
})
Control.displayName = "FormControl"

/**
 * Helper component to give form field an optional `<p>` tag description.
 * Connects it to form field for accessibility purposes.
 * @param {HTMLParagraphElement} props - extends `HTMLParagraphElement` properties
 */
const Description = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => {
  const { formDescription } = styles
  const { formDescriptionId } = useFormField()

  return (
    <p
      ref={ref}
      id={formDescriptionId}
      className={classNames(formDescription, className)}
      {...props}
    />
  )
})
Description.displayName = "FormDescription"

/**
 * Responsible for showing error and related messages to the user.
 * @param {HTMLParagraphElement} props - extends `HTMLParagraphElement` properties
 */
const Message = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, children, ...props }, ref) => {
    const { formMessage } = styles
    const { error, formMessageId } = useFormField()
    const body = error ? String(error?.message) : children

    if (!body) {
      return null
    }

    return (
      <p ref={ref} id={formMessageId} className={classNames(formMessage, className)} {...props}>
        {body}
      </p>
    )
  }
)
Message.displayName = "FormMessage"

export { Control, Description, Field, Item, Label, Message, Root, useFormField }
