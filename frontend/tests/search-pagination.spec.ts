import { test, expect } from "@playwright/test"

test.describe("Search Pagination", () => {
  test.beforeEach(async ({ page, context }) => {
    // Mock API responses for search
    const mockSearchResponse = {
      page: 1,
      pages: 5,
      per_page: 10,
      total: 50,
      results: Array.from({ length: 10 }, (_, i) => ({
        id: i + 1,
        type: "officer",
        name: `Officer ${i + 1}`
      }))
    }

    const mockSearchResponsePage2 = {
      page: 2,
      pages: 5,
      per_page: 10,
      total: 50,
      results: Array.from({ length: 10 }, (_, i) => ({
        id: i + 11,
        type: "officer",
        name: `Officer ${i + 11}`
      }))
    }

    // Intercept search API calls
    await page.route("**/api/v1/search/**", async (route) => {
      const url = route.request().url()
      const urlObj = new URL(url)
      const pageParam = urlObj.searchParams.get("page")

      // Return different response based on page parameter
      const response = pageParam === "2" ? mockSearchResponsePage2 : mockSearchResponse

      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(response)
      })
    })

    // Mock auth to return a token (search requires authentication)
    await page.route("**/api/v1/auth/**", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ access_token: "mock-token" })
      })
    })

    // Set up localStorage with auth token using context
    await context.addInitScript(() => {
      localStorage.setItem("access_token", "mock-token")
    })
  })

  test("URL updates when pagination page is changed", async ({ page }) => {
    // Navigate to search page with initial query
    await page.goto("/search?query=test&page=1")

    // Wait for pagination component to be visible and loaded
    const pagination = page.locator('[aria-label="pagination navigation"]')
    await expect(pagination).toBeVisible()

    // Wait for the page to be fully loaded
    await page.waitForLoadState("networkidle")

    // Click on page 2 button - use aria-label to be more specific
    const page2Button = pagination
      .getByRole("button", { name: "Go to page 2" })
      .or(pagination.getByRole("button", { name: "2" }).first())
    await expect(page2Button).toBeVisible()
    await page2Button.click()

    // Wait for URL to update with page=2
    await expect(page).toHaveURL(/.*page=2.*/, { timeout: 10000 })

    // Verify URL contains page=2
    const url = page.url()
    const urlObj = new URL(url)
    expect(urlObj.searchParams.get("page")).toBe("2")
  })

  test("API request is made when page changes via URL", async ({ page }) => {
    // Navigate to search page with initial query
    await page.goto("/search?query=test&page=1")
    await page.waitForLoadState("networkidle")

    // Set up promise to wait for API response with page=2
    const responsePromise = page.waitForResponse(
      (response) => {
        const url = response.url()
        return url.includes("/api/v1/search/") && url.includes("page=2")
      },
      { timeout: 10000 }
    )

    // Update URL directly using Next.js router (simulating URL change)
    // This should trigger the SearchProvider effect that watches searchParams
    await page.evaluate(() => {
      // Use Next.js router if available, otherwise use history API
      if ((window as any).next?.router) {
        ;(window as any).next.router.push("/search?query=test&page=2")
      } else {
        // Fallback: trigger popstate event which Next.js listens to
        window.history.pushState({}, "", "/search?query=test&page=2")
        window.dispatchEvent(new PopStateEvent("popstate"))
      }
    })

    // Wait for API request to be made
    const response = await responsePromise

    // Verify API request was made with page=2
    expect(response.ok()).toBe(true)
    const url = response.url()
    const urlObj = new URL(url)
    expect(urlObj.searchParams.get("page")).toBe("2")
  })

  test("UI updates when pagination page is changed", async ({ page }) => {
    // Navigate to search page with initial query
    await page.goto("/search?query=test&page=1")

    // Wait for pagination component to be visible
    const pagination = page.locator('[aria-label="pagination navigation"]')
    await expect(pagination).toBeVisible()
    await page.waitForLoadState("networkidle")

    // Verify initial page is highlighted (page 1) - use aria-current to find the active page
    const page1Button = pagination.locator('button[aria-current="page"]')
    await expect(page1Button).toHaveText("1")

    // Click on page 2 button - use more specific selector
    const page2Button = pagination
      .getByRole("button", { name: "Go to page 2" })
      .or(pagination.getByRole("button", { name: "2" }).first())
    await page2Button.click()

    // Wait for page 2 to be highlighted
    await expect(page2Button).toHaveAttribute("aria-current", "page", { timeout: 10000 })

    // Verify page 1 is no longer highlighted
    const newPage1Button = pagination
      .locator('button[aria-label="Go to page 1"]')
      .or(pagination.getByRole("button", { name: "1" }).first())
    await expect(newPage1Button).not.toHaveAttribute("aria-current", "page")
  })

  test("setPage updates URL and triggers API request", async ({ page }) => {
    // Navigate to search page with initial query first
    await page.goto("/search?query=test&page=1")
    await page.waitForLoadState("networkidle")

    // Set up promise to wait for API response with page=2 BEFORE clicking
    const responsePromise = page.waitForResponse(
      (response) => {
        const url = response.url()
        return url.includes("/api/v1/search/") && url.includes("page=2")
      },
      { timeout: 10000 }
    )

    // Click on page 2 in pagination
    const pagination = page.locator('[aria-label="pagination navigation"]')
    const page2Button = pagination
      .getByRole("button", { name: "Go to page 2" })
      .or(pagination.getByRole("button", { name: "2" }).first())
    await page2Button.click()

    // Wait for URL to update
    await expect(page).toHaveURL(/.*page=2.*/, { timeout: 10000 })

    // Wait for API request to be made
    const response = await responsePromise

    // Verify API request was made with page=2
    expect(response.ok()).toBe(true)
    const url = response.url()
    const urlObj = new URL(url)
    expect(urlObj.searchParams.get("page")).toBe("2")
  })
})
