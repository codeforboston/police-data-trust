module.exports = {
  stories: [
    "../stories/**/*.stories.mdx",
    "../stories/**/*.stories.@(js|jsx|ts|tsx)",
    "../compositions/**/*.stories.tsx",
    "../shared-components/**/*.stories.tsx"
  ],
  addons: ["@storybook/addon-links", "@storybook/addon-essentials"]
}
