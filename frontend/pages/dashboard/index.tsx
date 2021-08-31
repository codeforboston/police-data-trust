import * as React from "react"

import { useState } from "react"
import { BubbleChart, DashboardHeader, Map } from "../../compositions"
import { Layout } from "../../shared-components"
import { DataTable } from "../../shared-components/data-table/data-table"

type ChartType = "bubble" | "map"

export default function Dashboard() {
  const [whichChart, setWhichChart] = useState<ChartType>("bubble")

  const buttonStyle = {
    PointerEvents: "all",
    cursor: "pointer",
    margin: "2em 1em 1em 1em "
  }

  const VisChoiceButton = (buttonType: "bubble" | "map") => {
      return <button type="button" className={"primaryButton"} onClick={() => setWhichChart(buttonType)} style={buttonStyle}>
        {buttonType}
      </button>
}
  return (
    <Layout>
      <DashboardHeader />
      <div style={{display: "flex", flexDirection: "row", justifyContent: "center"}}>
        {VisChoiceButton("bubble")  }
        {VisChoiceButton("map")  }
      </div>
      {whichChart === "map" ? <Map /> : <BubbleChart />}
      <DataTable />
    </Layout>
  )
}

