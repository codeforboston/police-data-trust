import { Logo } from "../../../shared-components"
import styles from "./no-organizations.module.css"
import CreateOrganizationBtn from "../../../shared-components/create-organization-btn/create-organization-btn"

export default function NoOrganizations() {
  const { headerText } = styles

  return (
    <>
      <Logo />
      <h1 className={headerText}>You&apos;re currently Not Part of Any Organizations</h1>
      <CreateOrganizationBtn />
    </>
  )
}
