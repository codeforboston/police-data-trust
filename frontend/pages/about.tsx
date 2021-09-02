import * as React from 'react'

import { Layout } from "../shared-components"
import { DashboardHeader } from "../compositions"

// TODO: this is just a placeholder so navigation works

export default function AboutPage() {
  return (
    <Layout>
      <DashboardHeader />
      <div className="aboutPage" style={{margin: "1rem 3rem", textAlign: "center"}}>
        <h1>About Page</h1>
      </div>
    </Layout>
  )
}