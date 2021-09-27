import Profile from "../../pages/profile"
import { render } from "../test-utils"

it("renders Profile Page correctly", () => {
  const { container } = render(<Profile />)
  expect(container).toMatchSnapshot()
})
