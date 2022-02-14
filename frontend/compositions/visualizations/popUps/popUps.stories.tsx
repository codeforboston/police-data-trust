import { ComponentMeta, ComponentStory } from "@storybook/react"
import PopUp, { PopUpProps } from "./popUpComp"

export default {
  title: "Visualizations/PopUp",
  component: PopUp
} as ComponentMeta<typeof PopUp>

const Template: ComponentStory<typeof PopUp> = (args) => <PopUp {...args} />

export const Default = Template.bind({
  shouldShowPopUp: true,
  headerText: "test pop up",
  bodyText: "details info pop up",
  location: { x: 800, y: 600 }
})
