import { test, expect } from "@playwright/test"
import { ORGANIZATION_DETAILS } from "@/utils/constants"

test("homepage navigation links are rendered", async ({ page }) => {
  await page.goto("/")

  await expect(page.getByRole("navigation")).toBeVisible()
  await expect(page.getByRole("link", { name: /Home/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Search/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Overview/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /About/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Contact/i })).toBeVisible()
  await expect(page.getByText(ORGANIZATION_DETAILS.name).first()).toBeVisible()
})

test("about page includes nonprofit verification details", async ({ page }) => {
  await page.goto("/about")

  const { address } = ORGANIZATION_DETAILS

  await expect(page.getByRole("heading", { name: ORGANIZATION_DETAILS.name })).toBeVisible()
  await expect(page.getByText(ORGANIZATION_DETAILS.ein).first()).toBeVisible()
  await expect(page.getByText(address.street).first()).toBeVisible()
  await expect(page.getByText(address.suite).first()).toBeVisible()
  await expect(page.getByRole("link", { name: ORGANIZATION_DETAILS.email })).toBeVisible()
})
