import classNames from "classnames"
import { Dialog as D, PrimaryButton } from "../../shared-components"
import styles from "./create-organization-btn.module.css"
import CreateOrganizationForm from "./sub-comps/create-organization-form"

interface CreateOrganizationBtnProps {
  btnClassName?: string
}

export default function CreateOrganizationBtn({ btnClassName }: CreateOrganizationBtnProps) {
  const { triggerBtn } = styles

  return (
    <D.Root>
      <D.Trigger asChild>
        <PrimaryButton className={classNames(triggerBtn, btnClassName)}>
          Create Organization
        </PrimaryButton>
      </D.Trigger>
      <D.Content>
        <D.Header>
          <D.Title>Create Organization</D.Title>
          <D.Description>Create an organization if you don&apos;t already have one.</D.Description>
        </D.Header>
        <CreateOrganizationForm />
      </D.Content>
    </D.Root>
  )
}
