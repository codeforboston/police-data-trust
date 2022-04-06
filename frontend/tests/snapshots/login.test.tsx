import { AppRoutes } from "../../models"
import Login from "../../pages/login"
import { render, router, userEvent, waitFor } from "../test-utils"
import { act } from "react-dom/test-utils"

it("renders Login correctly", () => {
  const { container } = render(<Login />)
  expect(container).toMatchSnapshot()
})

describe("behaviors", () => {
  function renderPage() {
    const r = render(<Login />)
    const { getByRole, getByLabelText } = r

    return {
      ...r,
      email: getByRole("textbox", { name: /email address/i }),
      // https://github.com/testing-library/dom-testing-library/issues/567
      password: getByLabelText(/login password/i),
      submit: getByRole("button", { name: /submit/i })
    }
  }

  it("should require fields", async () => {
    const r = renderPage()
    act(() => {
      userEvent.click(r.submit)
    })

    await expect(r.findByText(/Please enter a valid email/i)).resolves.toBeInTheDocument()
    await expect(r.findByText(/A password is required/i)).resolves.toBeInTheDocument()
  })

  it("should reject invalid emails", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.email, "test@test")
      userEvent.type(r.password, "example")
      userEvent.click(r.submit)
    })

    await expect(r.findByText(/Please enter a valid email/i)).resolves.toBeInTheDocument()
  })

  it("should prompt the user on invalid credentials", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.email, "test@example.com")
      userEvent.type(r.password, "wrongpassword")
      userEvent.click(r.submit)
    })
    await expect(r.findByText(/Please check your email and password/i)).resolves.toBeInTheDocument()
  })

  it("should redirect on successful authentication", async () => {
    const r = renderPage()
    act(() => {
      userEvent.type(r.email, "test@example.com")
      userEvent.type(r.password, "password")
      userEvent.click(r.submit)
    })
    await waitFor(() => expect(router.pathname).toBe(AppRoutes.DASHBOARD))
  })
})
