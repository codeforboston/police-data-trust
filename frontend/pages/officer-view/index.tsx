import { DashboardHeader } from "../../compositions"
import  { OfficerHeader, OptionalOfficerInfo }  from "../../compositions/officer-view"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"

export default requireAuth(function OfficerView() {
    // const timothy = getOfficerFromMockData(0)
    return (
        <Layout>
            <DashboardHeader />
            <OfficerHeader {...getOfficerFromMockData(0)} />
            <hr/>
            <OptionalOfficerInfo  {...getOfficerFromMockData(0)} />
        </Layout>
    )
})



