import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import ExternalLink from "./external-link"


export default {
  title: "Shared Components/External LInk",
  component: ExternalLink
} as ComponentMeta<typeof ExternalLink>

const Template: ComponentStory<typeof ExternalLink> = (args) => <ExternalLink {...args} />

export const CodeForBostonLink = Template.bind({})
CodeForBostonLink.args = {
  linkPath: "https://codeforboston.org",
  linkText: "Code for Boston"
}
