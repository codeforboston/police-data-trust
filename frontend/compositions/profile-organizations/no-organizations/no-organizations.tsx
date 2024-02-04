import { Logo, PrimaryButton } from "../../../shared-components"
import styles from "./no-organizations.module.css"

export default function NoOrganizations() {
  const { headerText, organizationBtn } = styles

  return (
    <>
      <Logo />
      <h1 className={headerText}>You&apos;re currently Not Part of Any Organizations</h1>
      <PrimaryButton className={organizationBtn}>Create Organization</PrimaryButton>
    </>
  )
}
