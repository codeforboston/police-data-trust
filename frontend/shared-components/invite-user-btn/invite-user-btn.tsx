import classNames from "classnames"
import { Dialog as D, PrimaryButton } from "../../shared-components"
import styles from "./invite-user-btn.module.css"
import InviteUserForm from "./sub-comps/invite-user-form"

interface InviteUserBtnProps {
  btnClassName?: string
}

export default function InviteUserBtn({ btnClassName }: InviteUserBtnProps) {
  const { triggerBtn } = styles

  return (
    <D.Root>
      <D.Trigger asChild>
        <PrimaryButton className={classNames(btnClassName, triggerBtn)}>Invite User</PrimaryButton>
      </D.Trigger>
      <D.Content>
        <D.Header>
          <D.Title>Invite a User</D.Title>
          <D.Description>Invite a user to this organization.</D.Description>
        </D.Header>
        <InviteUserForm />
      </D.Content>
    </D.Root>
  )
}
