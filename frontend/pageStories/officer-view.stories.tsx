import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import OfficerView from "../pages/officer-view"
import officers from "../models/mock-data/officer.json"

export default {
    title: "Pages/OfficerView"
} as ComponentMeta<typeof OfficerView>

const Template: ComponentStory<typeof OfficerView> = (args) => <OfficerView {...args} />

export const Blank = Template.bind({})