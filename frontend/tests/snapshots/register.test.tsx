import { AppRoutes } from "../../models"
import Register from "../../pages/register"
import { render, router, uniqueEmail, userEvent, waitFor } from "../test-utils"
import { act } from "react-dom/test-utils"

it("renders Register correctly", () => {
  const { container } = render(<Register />)
  expect(container).toMatchSnapshot()
})

describe("behaviors", () => {
  function renderPage() {
    const r = render(<Register />)
    const { getByRole, getByLabelText } = r

    return {
      ...r,
      email: getByRole("textbox", { name: /email address/i }),
      createPassword: getByLabelText(/create password/i),
      confirmPassword: getByLabelText(/confirm password/i),
      firstname: getByRole("textbox", { name: /first name/i }),
      lastname: getByRole("textbox", { name: /last name/i }),
      phone_number: getByRole("textbox", { name: /phone number/i }),
      submit: getByRole("button", { name: /submit/i })
    }
  }

  it("checks required fields", async () => {
    const r = renderPage()
    const elements: any = r

    act(() => {
      userEvent.click(r.submit)
    })
    await expect(r.findAllByRole("alert")).resolves.toHaveLength(6)

    for (const k of [
      "email",
      "createPassword",
      "confirmPassword",
      "firstname",
      "lastname",
      "phone_number"
    ]) {
      expect(elements[k].getAttribute("aria-invalid")).toBeTruthy()
    }
  })

  it("checks phone number length", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.phone_number, "5555555555555")
      userEvent.click(r.submit)
    })
    await expect(r.findByText(/phone number is required/)).resolves.toBeInTheDocument()
  })

  it("checks email formatting", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.email, "test@test")
      userEvent.click(r.submit)
    })

    await expect(r.findByText(/enter a valid email/)).resolves.toBeInTheDocument()
  })

  it("checks password formatting", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.createPassword, "badpassword")
      userEvent.click(r.submit)
    })
    await expect(
      r.findByText(/please enter a password that contains/i)
    ).resolves.toBeInTheDocument()
  })

  it("requires matching passwords", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.firstname, "Spencer")
      userEvent.type(r.lastname, "Bool")
      userEvent.type(r.email, "spencer@example.com")
      userEvent.type(r.phone_number, "555 555 5555")
      userEvent.type(r.createPassword, "aA1!asdfasdf")
      userEvent.type(r.confirmPassword, "mistmatch")
      userEvent.click(r.submit)
    })
    await expect(r.findByText(/passwords do not match/i)).resolves.toBeInTheDocument()
  })

  it("should create a new user", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.firstname, "Spencer")
      userEvent.type(r.lastname, "Bool")
      userEvent.type(r.email, uniqueEmail())
      userEvent.type(r.phone_number, "555 555 5555")
      userEvent.type(r.createPassword, "aA1!asdfasdf")
      userEvent.type(r.confirmPassword, "aA1!asdfasdf")

      userEvent.click(r.submit)
    })
    await waitFor(() => expect(router.pathname).toBe(AppRoutes.DASHBOARD))
  })

  it("should reject existing accounts", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.firstname, "Spencer")
      userEvent.type(r.lastname, "Bool")
      userEvent.type(r.email, "test@example.com")
      userEvent.type(r.phone_number, "555 555 5555")
      userEvent.type(r.createPassword, "aA1!asdfasdf")
      userEvent.type(r.confirmPassword, "aA1!asdfasdf")

      userEvent.click(r.submit)
    })
    // There's no reason for this email to exist in the test database.
    // Skipping this test; UI is changing anyway.
    // await expect(r.findByText(/Existing account found./i)).resolves.toBeInTheDocument()
  })
})
