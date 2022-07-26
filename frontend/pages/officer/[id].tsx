import OfficerView from "../../compositions/officer-view"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"
import { useRouter } from "next/router"

export default requireAuth(function OfficerPage() {
  const router = useRouter()
  const id = parseInt(router.query.id as string)
  if (!isNaN(id)) {
    const officer = getOfficerFromMockData(id)
    return (
      <Layout>
        <OfficerView {...officer} />
      </Layout>
    )
  } else {
    return (
      <Layout>
        <p>Loading...</p>
      </Layout>
    )
  }

  // try {
  //   const id = parseInt(router.query.id as string)
  //   if (id == NaN) throw new Error()
  //   console.log(id)
  //   alert(id)
  //   const officer = getOfficerFromMockData(id)
  //   const tableProps = {
  //     tableName: "Involved Incidents",
  //     columns: resultsColumns,
  //     data: EXISTING_TEST_INCIDENTS
  //   }
  //   return (
  //     <Layout>
  //       <OfficerHeader {...officer} />
  //       <hr />
  //       <OptionalOfficerInfo {...officer} />
  //       <hr />
  //       <OfficerWorkHistory {...officer} />
  //       <OfficerAffiliations {...officer} />
  //       <DataTable {...tableProps} />
  //     </Layout>
  //   )
  // } catch (e) {
  //   console.error(e)
  //   return null
  // }
})
