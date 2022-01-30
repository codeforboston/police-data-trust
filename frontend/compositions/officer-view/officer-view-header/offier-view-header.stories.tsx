import { ComponentStory, ComponentMeta} from "@storybook/react"
import OfficerHeader from "./officer-view-header"
import officers from "../../../models/mock-data/officer.json"

export default {
    title: "Compositions/Officer View Components/OfficerHeader",
} as ComponentMeta<typeof OfficerHeader>

const Template: ComponentStory<typeof OfficerHeader> = (args) => <OfficerHeader {...args} />

export const Blank = Template.bind({})

export const Timothy = Template.bind({})
Timothy.args = officers[0]