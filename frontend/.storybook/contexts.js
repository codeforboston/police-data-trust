export const contexts = [
  {
    icon: "box", // a icon displayed in the Storybook toolbar to control contextual props
    title: "Themes", // an unique name of a contextual environment
    components: [
      // an array of components that is going to be injected to wrap stories
      /* Styled-components ThemeProvider, */
      /* Material-ui ThemeProvider, */
    ],
    params: [
      // an array of params contains a set of predefined `props` for `components`
      { name: "Light Theme", props: { theme /* : your light theme */ } },
      { name: "Dark Theme", props: { theme /* : your dark theme */ }, default: true }
    ],
    options: {
      deep: true, // pass the `props` deeply into all wrapping components
      disable: false, // disable this contextual environment completely
      cancelable: false // allow this contextual environment to be opt-out optionally in toolbar
    }
  }
  /* ... */ // multiple contexts setups are supported
]
