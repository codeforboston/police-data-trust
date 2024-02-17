import { zodResolver } from "@hookform/resolvers/zod"
import { useState } from "react"
import { FieldValues, useForm } from "react-hook-form"
import { z } from "zod"
import { Dialog as D, Form as F, Input, PrimaryButton } from "../../shared-components"
import styles from "./create-organization-form.module.css"
import {Select as S} from "../../shared-components"

interface SelectRoleProps{
    value: string
    onChange(...event: any[]): void
}

function SelectRole({value, onChange}: SelectRoleProps){
    return(
        <S.Root value = {value} onValueChange={onChange}>
            <S.Trigger>
                <S.Value placeholder = "Pick a role"/>
            </S.Trigger>
            <S.Content>
                <S.Item value="Publisher">Publisher</S.Item>
                <S.Item value="Member">Member</S.Item>
                <S.Item value="Admin">Admin</S.Item>
                <S.Item value="Subscriber">Subscriber</S.Item>
            </S.Content>
        </S.Root>
    )
}

type InviteUserSchema = z.infer<typeof inviteUserSchema>

const inviteUserSchema = z.object({
    userEmail: z.string().min(1, "Enter user email"),
    role: z.string()
})

export default function InviteUserForm(){

    const formMethods = useForm<InviteUserSchema>({
        resolver: zodResolver(inviteUserSchema),
        defaultValues: {
            userEmail:"",
            role: ""
        }
    })
    const [formCanSubmit, setFormCanSubmit] = useState(true)

    return(
        <F.Root formMethods = {formMethods} >
            <F.Field
                control={formMethods.control}
                name = "userEmail"
                render={({field})=>(
                    <F.Item>
                        <F.Label>User Email</F.Label>
                        <F.Control>
                            <Input type="text" {...field}/>
                        </F.Control>
                        <F.Message/>
                    </F.Item>
                )}
                
            />
            <F.Field
                control = {formMethods.control}
                name = "role"
                render={({field}) =>(
                    <F.Item>
                        <F.Label>Choose a role</F.Label>
                        <F.Control>
                            <SelectRole value={field.value} onChange={field.onChange}/>
                        </F.Control>
                        <F.Message/>
                    </F.Item>
                )}
            />
            <D.Footer>
                <PrimaryButton type = "submit">
                    Invite User
                </PrimaryButton>
            </D.Footer>
        </F.Root>
    )

}


