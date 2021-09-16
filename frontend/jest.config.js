/**
 * Modules under node_modules that use ESM modules and need to be transformed by
 * Babel. Jest runs in Node which does not support ESM modules by default. Most
 * libraries are distributed pre-transformed but these are not.
 */
const esmNodeModules = [
  "d3.*",
  "internmap",
  "delaunator",
  "robust-predicates",
  "node-fetch",
  "fetch-blob"
]

module.exports = {
  setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],
  // Ignore e2e tests which require a running backend
  testPathIgnorePatterns: ["<rootDir>/.next/", "<rootDir>/node_modules/", ".*e2e\\.test.*"],
  moduleNameMapper: {
    "\\.(scss|sass|css)$": "identity-obj-proxy"
  },
  testEnvironment: "jest-environment-jsdom",
  transformIgnorePatterns: [`node_modules/(?!(${esmNodeModules.join("|")})/)`]
}
