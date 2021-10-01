# Storybook Usage

Refer to [Official Documentation](https://storybook.js.org/docs/react/writing-stories/introduction) for more details.

In NPDC, stories can be written for any component in the `/compositions`, `/shared-components`, or `/pages` folders. Anything named `*.stories.tsx` in those folders will be rendered in the Storybook collection. To build locally, run the `storybook` script (`yarn storybook`). The result will be available at `http://localhost:6006`.

## Writing Stories

A Story is a way a component can be used - a component with props set to certain values. A component with many props can have many stories; one with no props will only have one default story.

For example, a story for a page that takes no props can be written like this:

```tsx
import React from "react"
import { Meta } from "@storybook/react"

export default {
  title: "Component Name",
  component: ComponentName
} as Meta<typeof ComponentName>

export const Default = <ComponentName />
```

Most of the stories in this project are slightly more complex. To facilitate multiple stories for each component, they've been written in Component Story Format (CSF), which features a named export for each story.

Below is a hypothetical component called `ComponentName`, in a file called `component-name.tsx`. The story would be in the same folder, and could be called `component-name.stories.tsx`:

```tsx
import React from "react"
import { ComponentMeta, ComponentStory } from "@storybook/react"
import ComponentName from "./component-name"

export default {
  title: "Folder/ComponentName",
  component: ComponentName
} as ComponentMeta<typeof ComponentName>

const Template: ComponentStory<typeof ComponentName> = (args) => <ComponentName {...args} />

export const Default = Template.bind({})
```

If there are different options available based on props, you can add them to the Default story like this:

```tsx
Default.args = {
  propName: value
}
```

Or you can create more stories:

```tsx
export const AnotherInstance = Template.bind({})
AnotherInstance.args = {
  propName: otherValue
}
```

## React Contexts

Components that incorporate useContext in some way need a Decorator. For example, any component that references `useFormContext` from `react-hook-form` needs to have the `FormProvider` decorator available, or the story will crash.

### Decorator Syntax

Context decorators can be added to the default export, like this:

```tsx
export default {
  title: "Folder/ComponentName",
  component: ComponentName,
  decorators: [
    (Story) => (
      <Provider>
        <Story />
      </Provider>
    )
  ]
}
```

### Context Providers

Non-exhaustive list of Context Providers - if your component uses the context (or references something that does), the Story will need a decorator that wraps it in the following provider:

| Context        | Provider     | Package           |
| -------------- | ------------ | ----------------- |
| useForm        | FormProvider | react-hook-form   |
| useFormContext | FormProvider | react-hook-form   |
| useAuth        | AuthProvider | /helpers/api/auth |
