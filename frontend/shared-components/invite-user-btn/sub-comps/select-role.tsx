import { Select as S } from "../../../shared-components"
import { UserRoles } from "../../../models/profile"
import { capitalizeFirstChar } from "../../../helpers"

const userRoles = Object.keys(UserRoles).filter((el) => isNaN(Number(el)))

interface SelectRoleProps {
  value: string
  onChange(...event: any[]): void
}

export default function SelectRole({ value, onChange }: SelectRoleProps) {
  return (
    <S.Root value={value} onValueChange={onChange}>
      <S.Trigger>
        <S.Value placeholder="Pick the user's role" />
      </S.Trigger>
      <S.Content>
        {userRoles.map((role) => (
          <S.Item key={role} value={role}>
            {capitalizeFirstChar(role.toLowerCase())}
          </S.Item>
        ))}
      </S.Content>
    </S.Root>
  )
}
