import { ProfileInfo } from "../../compositions"
import { render } from "../test-utils"

it("renders Profile Info section correctly", () => {
  const { container } = render(<ProfileInfo />)
  expect(container).toMatchSnapshot()
})