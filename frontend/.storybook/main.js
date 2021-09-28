module.exports = {
  stories: [
    "../compositions/**/*.stories.tsx",
    "../shared-components/**/*.stories.tsx",
    "../pages/**/*.stories.tsx"
  ],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "storybook-css-modules-preset",
    "storybook-addon-next-router"
  ]
}
