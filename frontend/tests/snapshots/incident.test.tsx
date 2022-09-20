import { render } from "../test-utils"
import IncidentView from "../../compositions/incident-view"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"
import { Incident } from "../../helpers/api"

describe("Incident Page", () => {
  it("Renders the incident page correctly", () => {
    const sampleIncident: Incident = {
      id: 0,
      time_of_incident: "March 1, 2022",
      longitude: -71.0589,
      latitude: 42.3601,
      description:
        "Officer issued motorist ticket, use of excessive force resulted in civilian injury.",
      officers: [
        { first_name: "George", last_name: "Lopez" },
        { first_name: "Hannah", last_name: "Montana" }
      ]
    }

    const tree = render(<IncidentView {...sampleIncident} />)
    expect(tree).toMatchSnapshot()
  })
})
