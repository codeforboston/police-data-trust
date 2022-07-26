import { ComponentMeta, ComponentStory } from "@storybook/react"
import OfficerView from "../pages/officer/[id]"

export default {
  title: "Pages/OfficerView"
} as ComponentMeta<typeof OfficerView>

const Template: ComponentStory<typeof OfficerView> = () => <OfficerView />

export const Timothy = Template.bind({})
