import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import { Providers } from "../../helpers"
import ViewerRegistration from "."

export default {
  title: "Pages/Registration",
  component: ViewerRegistration,
  decorators: [
    (Story) => (
      <Providers>
        <Story />
      </Providers>
    )
  ]
} as ComponentMeta<typeof ViewerRegistration>

const Template: ComponentStory<typeof ViewerRegistration> = (args) => (
  <ViewerRegistration {...args} />
)

export const Register = Template.bind({})
Register.parameters = {
  controls: { hideNoControlsWarning: true }
}
