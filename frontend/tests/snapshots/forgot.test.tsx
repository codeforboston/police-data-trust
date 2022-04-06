import { AppRoutes } from "../../models"
import ForgotPassword from "../../pages/forgot"
import { render, router, userEvent, waitFor } from "../test-utils"
import { act } from "react-dom/test-utils"

it("renders Forgot correctly", () => {
  const { container } = render(<ForgotPassword />)
  expect(container).toMatchSnapshot()
})

describe("behaviors", () => {
  function renderPage() {
    const r = render(<ForgotPassword />)
    const { getByRole } = r

    return {
      ...r,
      email: getByRole("textbox", { name: /email address/i }),
      submit: getByRole("button", { name: /submit/i })
    }
  }

  it("should require fields", async () => {
    const r = renderPage()
    act(() => {
      userEvent.click(r.submit)
    })
    await expect(r.findByText(/Please enter a valid email/i)).resolves.toBeInTheDocument()
  })

  it("should reject invalid emails", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.email, "test@test")
      userEvent.click(r.submit)
    })
    await expect(r.findByText(/Please enter a valid email/i)).resolves.toBeInTheDocument()
  })

  it("should show success on valid email", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.email, "test@example.com")
      userEvent.click(r.submit)
    })
    await expect(r.findByText(/Success!/i)).resolves.toBeInTheDocument()
  })

  it("should show success on invalid email", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.email, "thisemail@doesnotexist.com")
      userEvent.click(r.submit)
    })
    await expect(r.findByText(/Success!/i)).resolves.toBeInTheDocument()
  })
})
