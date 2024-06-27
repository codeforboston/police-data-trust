module.exports = {
  presets: ["next/babel"],
  plugins: ["inline-react-svg"],
  env: {
    test: {
      plugins: ["transform-dynamic-import"]
    }
  }
}
