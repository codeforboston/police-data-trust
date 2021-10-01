import { EditProfileInfo } from "../../compositions"
import { render } from "../test-utils"

it("renders Edit Profile Info section correctly", () => {
  const { container } = render(<EditProfileInfo cancelEditMode={null} />)
  expect(container).toMatchSnapshot()
})
