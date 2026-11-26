import { act, cleanup, fireEvent, render, screen } from "@testing-library/react"
import { afterEach, expect, test, vi } from "vitest"
import DonateButton from "./donateButton"

const script = vi.hoisted(() => ({
  onReady: undefined as (() => void) | undefined,
  onError: undefined as (() => void) | undefined
}))

vi.mock("next/script", () => ({
  default: (props: typeof script) => {
    script.onReady = props.onReady
    script.onError = props.onError
    return null
  }
}))

afterEach(() => {
  cleanup()
  delete window.PayPal
})

test("renders the production button once and renders again after returning to the page", () => {
  const donate = vi.fn()
  const renderButton = vi.fn((selector: string) => {
    const image = document.createElement("img")
    image.id = "donate-button"
    image.alt = "Donate with PayPal button"
    image.addEventListener("click", donate)
    document.querySelector(selector)?.appendChild(image)
  })
  const Button = vi.fn(() => ({ render: renderButton }))
  window.PayPal = { Donation: { Button } }

  const firstVisit = render(<DonateButton />)
  act(() => script.onReady?.())
  act(() => script.onReady?.())

  expect(Button).toHaveBeenCalledTimes(1)
  expect(Button).toHaveBeenCalledWith({
    env: "production",
    hosted_button_id: "KWDM4H3KATHA2",
    image: {
      src: "https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif",
      alt: "Donate with PayPal button",
      title: "PayPal - The safer, easier way to pay online!"
    }
  })
  expect(renderButton).toHaveBeenCalledWith("#donate-button")

  const button = screen.getByRole("button", { name: "Donate with PayPal button" })
  expect(button.tabIndex).toBe(0)
  expect(document.querySelectorAll("#donate-button")).toHaveLength(1)
  fireEvent.keyDown(button, { key: "Enter" })
  fireEvent.keyDown(button, { key: " " })
  expect(donate).toHaveBeenCalledTimes(2)

  firstVisit.unmount()
  render(<DonateButton />)
  act(() => script.onReady?.())
  expect(Button).toHaveBeenCalledTimes(2)
})

test("keeps a direct donation link available before the SDK loads and on load failure", () => {
  render(<DonateButton />)
  const directLink = screen.getByRole("link", { name: "Donate directly on PayPal" })
  expect(directLink.getAttribute("href")).toBe(
    "https://www.paypal.com/donate/?hosted_button_id=KWDM4H3KATHA2"
  )

  act(() => script.onError?.())
  expect(screen.getByRole("status").textContent).toContain("couldn’t load")
  expect(screen.getByRole("link", { name: "Donate directly on PayPal" })).toBe(directLink)
})

test("handles an unavailable SDK or a failed button render", () => {
  const visit = render(<DonateButton />)
  act(() => script.onReady?.())
  expect(screen.getByRole("status").textContent).toContain("couldn’t load")
  visit.unmount()

  window.PayPal = {
    Donation: {
      Button: () => ({
        render: () => {
          throw new Error("SDK render failure")
        }
      })
    }
  }
  render(<DonateButton />)
  act(() => script.onReady?.())
  expect(screen.getByRole("status").textContent).toContain("couldn’t load")
})
