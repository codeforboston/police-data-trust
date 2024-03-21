import { ComponentMeta, ComponentStory } from "@storybook/react"
import Dashboard from "../pages/search"

export default {
  title: "Pages/Dashboard",
  component: Dashboard
} as ComponentMeta<typeof Dashboard>

const Template: ComponentStory<typeof Dashboard> = (args: any) => <Dashboard {...args} />

export const Default = Template.bind({})
