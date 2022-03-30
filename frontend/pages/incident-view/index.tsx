import { DashboardHeader } from "../../compositions"
import { requireAuth } from "../../helpers"
import { Layout } from "../../shared-components"
import { IncidentViewHeader } from '../../compositions/incident-view'

export default requireAuth(function() {

    return (
        <Layout>
            <DashboardHeader />
        </Layout>
    )
}

)