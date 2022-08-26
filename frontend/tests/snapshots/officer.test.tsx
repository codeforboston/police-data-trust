import { render } from "../test-utils"
import OfficerView from "../../compositions/officer-view"
import { getOfficerFromMockData } from "../../helpers/mock-to-officer-type"

describe("Officer Page", () => {
  it("Renders the officer page correctly", () => {
    const tree = render(<OfficerView {...getOfficerFromMockData(0)} />)
    expect(tree).toMatchSnapshot()
  })
})
