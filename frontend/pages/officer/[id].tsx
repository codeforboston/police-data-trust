import OfficerView from "../../compositions/officer-view"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"
import { useRouter } from "next/router"

export default requireAuth(function OfficerPage() {
  const router = useRouter()
  const id = parseInt(router.query.id as string)
  return isNaN(id) ? <p>Loading</p> : <OfficerView {...getOfficerFromMockData(id)} />
})
