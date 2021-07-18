import * as React from 'react';
import { passwordToggleViews } from '../models/password-aid'
// Usage
function App() {
  // Call the hook which returns, current value and the toggler function
  const [isTextChanged, setIsTextChanged] = useToggle()
  return <button onClick={setIsTextChanged}>{isTextChanged ? "Toggled" : "Click to Toggle"}</button>
}
// The toggled password view is comprised of the current icon to be displayed, the shown text, and whether or not it needs to be hidden

// Hook
// Parameter is the boolean, with default "false" value
export const useToggle = (initialState: boolean = false): [boolean, any] => {
  // Initialize the state
  const [state, setState] = React.useState<boolean>(initialState)
  // Define and memorize toggler function in case we pass down the comopnent,
  // This function change the boolean value to it's opposite value
  const toggle = React.useCallback((): void => setState((state) => !state), [])
  return [state, toggle]
}

/* Lifecycle, from back to front:

- The password aid component is passed down to the viewer registration component
- The password aid component takes props, and renders as appropriate.

*/


