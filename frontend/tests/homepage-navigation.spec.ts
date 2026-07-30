import { test, expect } from "@playwright/test"

test("homepage navigation links are rendered", async ({ page }) => {
  await page.goto("/")

  await expect(page.getByRole("navigation")).toBeVisible()
  await expect(page.getByRole("link", { name: /Home/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Search/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Overview/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /About/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Contact/i })).toBeVisible()
  await expect(page.getByText("National Police Data Coalition").first()).toBeVisible()
})

test("about page includes nonprofit verification details", async ({ page }) => {
  await page.goto("/about")

  await expect(page.getByRole("heading", { name: "National Police Data Coalition" })).toBeVisible()
  await expect(page.getByText("87-4427926").first()).toBeVisible()
  await expect(page.getByText("4201 Main St").first()).toBeVisible()
  await expect(page.getByRole("link", { name: "info@nationalpolicedata.org" })).toBeVisible()
})
