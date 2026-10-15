import React from "react"
import { afterEach, describe, expect, it } from "vitest"
import { cleanup, render, screen } from "@testing-library/react"
import OfficerIdentityCard from "@/components/Details/IdentityCard/OfficerIdentityCard"
import EmploymentTimeline from "@/components/Details/EmploymentTimeline"
import { Officer } from "@/utils/api"

const officer = {
  uid: "officer-1",
  first_name: "Robert",
  middle_name: "P",
  last_name: "Sears",
  employment_history: []
} as unknown as Officer

afterEach(cleanup)

describe("Employment Record Missing", () => {
  it("labels an officer with no employment records", () => {
    render(<OfficerIdentityCard officer={officer} />)

    expect(screen.getByText("Employment Record Missing")).toBeTruthy()
  })

  it("adds no label when employment records were not loaded", () => {
    render(<OfficerIdentityCard officer={{ ...officer, employment_history: undefined }} />)

    expect(screen.queryByText("Employment Record Missing")).toBeNull()
  })

  it("labels an empty employment timeline", () => {
    render(<EmploymentTimeline employment_history={[]} />)

    expect(screen.getByText("Employment Record Missing")).toBeTruthy()
  })
})
