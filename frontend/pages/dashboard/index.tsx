import * as React from "react"

import { useState } from "react"
import { DashboardHeader } from "../../compositions"
import { Map } from "../../compositions"

import { Layout } from "../../shared-components"
import { DataTable } from "../../shared-components/data-table/data-table"

type ChartType = "bubble" | "map"

export default function Dashboard() {
  const [whichChart, setWhichChart] = useState<ChartType>("bubble")

  const buttonStyle = {
    PointerEvents: "all",
    cursor: "pointer",
    marginTop: "2em"
  }

  const VisChoiceButton = (buttonType: "bubble" | "map") => {
    return (
      <button
        type="button"
        className={"primaryButton"}
        onClick={() => setWhichChart(buttonType)}
        style={buttonStyle}>
        {buttonType}
      </button>
    )
  }
  return (
    <Layout>
      <DashboardHeader />
      <Map />
      <DataTable />
    </Layout>
  )
}
