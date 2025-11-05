import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  /* config options here */
  output: "export"
}

module.exports = {
  allowedDevOrigins: ["http://localhost:3000", "http://127.0.0.1:3000", "127.0.0.1"]
}

export default nextConfig
