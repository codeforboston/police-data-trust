import Profile from "../../pages/profile"
import { render, setAuthForTest } from "../test-utils"

beforeAll(() => setAuthForTest())

it("renders Profile Page correctly", () => {
  const { container } = render(<Profile />)
  expect(container).toMatchSnapshot()
})
