import { defineConfig } from "@playwright/test"

const port = process.env.NPDI_WEB_PORT || 3000
const baseURL = `http://localhost:${port}`

export default defineConfig({
  use: {
    baseURL
  },
  testDir: "./tests"
})
