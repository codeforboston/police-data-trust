import classNames from "classnames"
import {Dialog as D, PrimaryButton} from "../../../shared-components"
import styles from "./invite-user-button.module.css"
import InviteUserForm from "./invite-user-form"

interface InviteUserBtnProps{
    btnClassName?: string
}

export default function InviteUserBtn({btnClassName}: InviteUserBtnProps){
    const {triggerBtn} = styles

    return(
        <D.Root>
            <D.Trigger asChild>
                <PrimaryButton className={classNames(triggerBtn, btnClassName)}>
                    Invite User
                </PrimaryButton>
            </D.Trigger>
            <D.Content>
                <D.Header>
                    <D.Title>Invite User</D.Title>
                </D.Header>
                <InviteUserForm/>
            </D.Content>
        </D.Root>
    )
}