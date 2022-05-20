import * as React from "react"
import { Map } from "../../compositions"
import { render, setAuthForTest, waitFor } from "../test-utils"

describe("the map", () => {
  beforeAll(() => setAuthForTest())

  it("renders Map correctly", async () => {
    const { container, findByTitle } = render(<Map />)
    await waitFor(() => expect(findByTitle("New York")).resolves.toBeInTheDocument())

    expect(container).toMatchSnapshot()
  })
})
