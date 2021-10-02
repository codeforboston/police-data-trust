import React from "react"
import { ComponentStory, ComponentMeta } from "@storybook/react"
import { USAStateInput } from ".."
import { Providers } from "../../helpers"

export default {
  title: "Shared Components/State Input",
  component: USAStateInput,
  decorators: [
    (Story) => (
      <Providers>
        <Story />
      </Providers>
    )
  ]
} as ComponentMeta<typeof USAStateInput>

const Template: ComponentStory<typeof USAStateInput> = (args) => <USAStateInput {...args} />

export const Default = Template.bind({})
