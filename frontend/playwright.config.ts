import { defineConfig } from "@playwright/test"

const port = process.env.NPDI_WEB_PORT || 3000
const baseURL = `http://localhost:${port}`

export default defineConfig({
  use: {
    baseURL,
    // Capture screenshots on failure
    screenshot: "only-on-failure",
    // Capture video on failure
    video: "retain-on-failure"
  },
  testDir: "./tests",
  testMatch: "**/*.spec.ts",
  // Configure output directories
  outputDir: "test-results",
  // Configure reporters
  reporter: [["html", { outputFolder: "playwright-report", open: "never" }], ["list"]],
  // In CI, docker compose runs the server, so we don't need Playwright to start one
  // In local development, Playwright will start the dev server
  ...(process.env.CI
    ? {}
    : {
        webServer: {
          command: `npm run dev`,
          port: Number(port),
          reuseExistingServer: true,
          timeout: 120 * 1000,
          env: {
            NPDI_WEB_PORT: String(port)
          }
        }
      })
})
