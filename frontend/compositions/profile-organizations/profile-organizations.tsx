import { useAuth } from "../../helpers"
import NoOrganizations from "./no-organizations/no-organizations"
import styles from "./profile-organizations.module.css"

export default function ProfileOrganizations() {
  const { organizationContainer, headerText, organizationBtn } = styles
  const { user } = useAuth()

  // TODO: Find user's organizations (if any)
  // API endpoint needed: Given a user, get their partners

  // TODO: Separate UI for:
  // 2. Existing Organizations

  return (
    <section className={organizationContainer}>
      <NoOrganizations />
    </section>
  )
}
