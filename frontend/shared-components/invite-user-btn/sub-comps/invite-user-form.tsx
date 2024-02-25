import { zodResolver } from "@hookform/resolvers/zod"
import { FieldValues, useForm } from "react-hook-form"
import { z } from "zod"
import { UserRoles } from "../../../models/profile"
import { Form as F, Input, Dialog as D, PrimaryButton } from "../../../shared-components"
import SelectRole from "./select-role"
import styles from "./invite-user-form.module.css"

type UserRolesKeys = keyof typeof UserRoles

type InviteUserSchema = z.infer<typeof inviteUserSchema>
const inviteUserSchema = z.object({
  email: z.string().email(),
  role: z.enum(Object.keys(UserRoles) as [UserRolesKeys])
})

export default function InviteUserForm() {
  const { submitBtn } = styles

  const formMethods = useForm<InviteUserSchema>({
    resolver: zodResolver(inviteUserSchema),
    defaultValues: {
      email: "",
      role: "NONE"
    }
  })

  const onSubmit = (values: FieldValues) => {
    console.log("values: ", values)
  }

  return (
    <F.Root formMethods={formMethods} onSubmit={formMethods.handleSubmit(onSubmit)}>
      <F.Field
        control={formMethods.control}
        name="email"
        render={({ field }) => (
          <F.Item>
            <F.Label>User&apos;s email</F.Label>
            <F.Control>
              <Input type="text" {...field} />
            </F.Control>
            <F.Message />
          </F.Item>
        )}
      />
      <F.Field
        control={formMethods.control}
        name="role"
        render={({ field }) => (
          <F.Item>
            <F.Label>User&apos;s role</F.Label>
            <F.Control>
              <SelectRole value={field.value} onChange={field.onChange} />
            </F.Control>
          </F.Item>
        )}
      />
      <D.Footer>
        <PrimaryButton type="submit" className={submitBtn}>
          Invite User
        </PrimaryButton>
      </D.Footer>
    </F.Root>
  )
}
