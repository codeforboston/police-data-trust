import { Select as S } from "../../../shared-components"

interface SelectOrgProps {
  value: string
  onChange(...event: any[]): void
}

export default function SelectOrg({ value, onChange }: SelectOrgProps) {
  return (
    <S.Root value={value} onValueChange={onChange}>
      <S.Trigger>
        <S.Value placeholder="Pick an organization if it's yours..." />
      </S.Trigger>
      <S.Content>
        <S.Item value="organization1">Organization1</S.Item>
        <S.Item value="organization2">Organization2</S.Item>
        <S.Item value="organization3">Organization3</S.Item>
      </S.Content>
    </S.Root>
  )
}
