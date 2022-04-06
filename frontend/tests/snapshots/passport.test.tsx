import * as React from "react"
import Passport from "../../pages/passport/index"
import { render, setAuthForTest, userEvent } from "../test-utils"
import { act } from "react-dom/test-utils"

beforeAll(() => setAuthForTest())

it("renders Passport correctly", () => {
  const { container } = render(<Passport />)
  expect(container).toMatchSnapshot()
})

describe("behaviors", () => {
  function renderPage() {
    const r = render(<Passport />)
    const { getByRole } = r

    return {
      ...r,
      address: getByRole("textbox", { name: /street address/i }),
      city: getByRole("textbox", { name: /city or town/i }),
      state: getByRole("combobox", { name: /state/i }),
      zip: getByRole("spinbutton", { name: /zip code/i }),
      reason: getByRole("textbox", { name: /why are you signing up to the npdc/i }),
      submit: getByRole("button", { name: /submit/i })
    }
  }

  it("submits the form", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.address, "123 Park Street")
      userEvent.type(r.city, "Boston")
      userEvent.type(r.state, "MA")
      userEvent.type(r.zip, "02155")
      userEvent.type(r.reason, Array(10).fill("In a partner organization ").join(""))

      userEvent.click(r.submit)
    })

    await expect(r.findByText(/thank you for your submission/i)).resolves.toBeInTheDocument()
  })
})
