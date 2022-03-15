import { api, useAuth } from "../../helpers"
import { act } from "react-dom/test-utils"
import { EXISTING_TEST_USER } from "../../helpers/api/mocks/data"
import { AppRoutes } from "../../models"
import Reset from "../../pages/reset"
import { render, router, setAuthForTest, uniqueEmail, userEvent, waitFor } from "../test-utils"

it("renders Register correctly", () => {
  const { container } = render(<Reset />)
  expect(container).toMatchSnapshot()
})

describe("behaviors", () => {
  function renderPage() {
    const r = render(<Reset />)
    const { getByRole, getByLabelText } = r

    return {
      ...r,
      createPassword: getByLabelText(/create password/i),
      confirmPassword: getByLabelText(/confirm password/i),
      submit: getByRole("button", { name: /submit/i })
    }
  }

  it("checks required fields", async () => {
    const token = await api.login(EXISTING_TEST_USER)

    const useRouter = jest.spyOn(require("next/router"), "useRouter")
    const mockPush = jest.fn()

    setAuthForTest()

    useRouter.mockImplementation(() => ({
      route: "/reset",
      pathname: "",
      query: { token: token },
      asPath: "",
      push: mockPush,
      events: {
        on: jest.fn(),
        off: jest.fn()
      },
      beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    }))

    const r = renderPage()
    const elements: any = r

    act(() => userEvent.click(r.submit))

    for (const k of ["createPassword", "confirmPassword"]) {
      expect(elements[k].getAttribute("aria-invalid")).toBeTruthy()
    }

    expect(r.findAllByRole("alert")).resolves.toHaveLength(2)
  })

  it("checks password formatting", async () => {
    const r = renderPage()

    act(() => {
      userEvent.type(r.createPassword, "badpassword")
      userEvent.click(r.submit)
    })

    expect(r.findAllByRole("alert")).resolves.toHaveLength(2)
  })

  it("requires matching passwords", async () => {
    const r = renderPage()

    act(() => {
      userEvent.type(r.createPassword, "aA1!asdfasdf")
      userEvent.type(r.confirmPassword, "mistmatch")
      userEvent.click(r.submit)
    })

    await expect(r.findByText(/passwords do not match/i)).resolves.toBeInTheDocument()
  })

  it("should redirect to the login", async () => {
    const token = await api.login(EXISTING_TEST_USER)

    const useRouter = jest.spyOn(require("next/router"), "useRouter")
    const mockPush = jest.fn()

    setAuthForTest()

    useRouter.mockImplementation(() => ({
      route: "/reset",
      pathname: "",
      query: { token: token },
      asPath: "",
      push: mockPush,
      events: {
        on: jest.fn(),
        off: jest.fn()
      },
      beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    }))

    const r = renderPage()

    act(() => {
      userEvent.type(r.createPassword, "aA1!asdfasdf")
      userEvent.type(r.confirmPassword, "aA1!asdfasdf")
      userEvent.click(r.submit)
    })

    await waitFor(() => expect(mockPush).toHaveBeenCalledWith(AppRoutes.LOGIN))
  })

  it("checks token validity", async () => {
    const token = await api.login(EXISTING_TEST_USER)

    const useRouter = jest.spyOn(require("next/router"), "useRouter")
    const mockPush = jest.fn()

    setAuthForTest()

    useRouter.mockImplementation(() => ({
      route: "/reset",
      pathname: "",
      query: { token: "badtoken" },
      asPath: "",
      push: mockPush,
      events: {
        on: jest.fn(),
        off: jest.fn()
      },
      beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    }))

    const r = renderPage()

    act(() => {
      userEvent.type(r.createPassword, "aA1!asdfasdf")
      userEvent.type(r.confirmPassword, "aA1!asdfasdf")
      userEvent.click(r.submit)
    })

    await expect(
      r.findByText(/Token Invalid, please request another forgot password email/i)
    ).resolves.toBeInTheDocument()
  })
})
