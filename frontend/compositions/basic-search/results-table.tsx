import { useSearch } from "../../helpers"

export function ResultsTable() {
  const { incidentResults } = useSearch()

  return incidentResults ? <JsonDump json={incidentResults} /> : null
}

const JsonDump = ({ json }: any) => (
  <section
    style={{
      maxWidth: "500px",
      margin: "1em auto"
    }}
  >
    <h1>Search Results</h1>
    <pre
      style={{
        whiteSpace: "pre-wrap",
        maxHeight: "500px",
        overflowY: "scroll"
      }}
    >
      {JSON.stringify(json, null, 2)}
    </pre>
  </section>
)
