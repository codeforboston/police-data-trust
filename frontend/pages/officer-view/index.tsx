import { DashboardHeader } from "../../compositions"
import  OfficerHeader  from "../../compositions/officer-view/officer-view-header/officer-view-header"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"

export default requireAuth(function OfficerView() {
    return (
        <Layout>
            <DashboardHeader />
            <OfficerHeader {...getOfficerFromMockData(0)} />
        </Layout>
    )
})



