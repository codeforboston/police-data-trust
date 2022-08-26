import { render } from "../test-utils"
import IncidentView from "../../compositions/incident-view"
import getIncident from "../../helpers/incident"

describe("Incident Page", () => {
  it("Renders the incident page correctly", () => {
    const tree = render(<IncidentView {...getIncident(0)} />)
    expect(tree).toMatchSnapshot()
  })
})
