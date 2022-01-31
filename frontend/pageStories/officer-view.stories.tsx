import { ComponentMeta, ComponentStory } from "@storybook/react"
import OfficerView from "../pages/officer-view"

export default {
    title: "Pages/OfficerView"
} as ComponentMeta<typeof OfficerView>

const Template: ComponentStory<typeof OfficerView> = (args) => <OfficerView {...args} />

export const Timothy = Template.bind({})
