const base = require("./jest.config")

module.exports = {
  ...base,
  testPathIgnorePatterns: base.testPathIgnorePatterns.filter((p) => !p.includes("e2e")),
  testMatch: ["**/*.e2e.test.[jt]s?(x)"]
}
