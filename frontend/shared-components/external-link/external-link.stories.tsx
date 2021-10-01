import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import ExternalLink from "./external-link"

export default {
  title: "Shared Components/External Link",
  component: ExternalLink
} as ComponentMeta<typeof ExternalLink>

const Template: ComponentStory<typeof ExternalLink> = (args) => <ExternalLink {...args} />

export const Default = Template.bind({})
Default.args = {
  linkPath: "http://example.com",
  linkText: "Example"
}
