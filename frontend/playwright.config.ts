import { defineConfig } from "@playwright/test"

const port = process.env.NPDI_WEB_PORT || 3000
const baseURL = `http://localhost:${port}`

export default defineConfig({
  use: {
    baseURL
  },
  testDir: "./tests",
  testMatch: "**/*.spec.ts",
  webServer: {
    command: `npm run dev`,
    port: Number(port),
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
    env: {
      NPDI_WEB_PORT: String(port)
    }
  }
})
