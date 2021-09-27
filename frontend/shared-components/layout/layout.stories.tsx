import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { Layout } from ".."

export default {
  title: "Shared Components/Layout",
  component: Layout
} as ComponentMeta<typeof Layout>

const Template: ComponentStory<typeof Layout> = (args) => <Layout {...args} />

export const DefaultLayout = Template.bind({})
