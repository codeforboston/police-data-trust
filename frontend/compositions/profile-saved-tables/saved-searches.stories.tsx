import React from "react"
import { ComponentMeta } from "@storybook/react"
import SavedSearches from "./saved-searches"
// import { mockSavedSearches } from "../../models/mock-data"

export default {
  title: "Compositions/Saved Searches",
  component: SavedSearches
} as ComponentMeta<typeof SavedSearches>

export const Default = <SavedSearches />
