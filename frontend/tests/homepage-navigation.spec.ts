import { test, expect } from "@playwright/test"

test("homepage navigation links are rendered", async ({ page }) => {
  await page.goto("/")

  // Example selectors - update these to match your actual navigation links
  await expect(page.getByRole("navigation")).toBeVisible()
  await expect(page.getByRole("link", { name: /Home/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Data Explorer/i })).toBeVisible()
  await expect(page.getByRole("link", { name: /Community/i })).toBeVisible()
})
