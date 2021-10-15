import React from "react"
import { ComponentMeta } from "@storybook/react"
import SavedResults from "./saved-results"
import { mockSavedResults } from "../../models/mock-data"


export default {
  title: "Compositions/Saved Results",
  component: SavedResults
} as ComponentMeta<typeof SavedResults>

export const Default = <SavedResults data={mockSavedResults} />
