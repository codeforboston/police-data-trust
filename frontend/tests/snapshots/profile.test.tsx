import { ProfileMenu } from "../../models/profile"
import Profile from "../../pages/profile"
import { render, setAuthForTest } from "../test-utils"

beforeAll(() => setAuthForTest())

it("renders Profile Page correctly", () => {
  const { container } = render(<Profile initialTab={ProfileMenu.USER_INFO} />)
  expect(container).toMatchSnapshot()
})
