import ContentDetails from "./ContentDetails"
import { Agency } from "@/utils/api"
import { getSourceHref } from "@/utils/sourceRoutes"

type AgencyContentDetailsProps = {
  agency: Agency
}

export default function AgencyContentDetails({ agency }: AgencyContentDetailsProps) {
  const totalComplaints = agency.total_complaints || 0

  const totalOfficers = agency.total_officers || 0

  const dataSources =
    agency.sources?.flatMap((source) => {
      if (!source.name) return []

      const href = getSourceHref(source)
      if (!href) return []

      return [
        {
          label: source.name,
          href
        }
      ]
    }) || []

  return (
    <ContentDetails
      contentType="Agency"
      dataSources={dataSources}
      lastUpdatedText="Nov 1, 2024 by"
      lastUpdatedBy="Adam Zelitzky"
      summaryItems={[
        { label: "Officers", value: String(totalOfficers) },
        { label: "Complaints", value: String(totalComplaints) },
        { label: "Related Articles", value: "0" }
      ]}
      associatedTitle="Associated officers"
      associatedPeople={[
        { name: "Adam Zelitzky" },
        { name: "Andrew Damora" },
        { name: "John Dadamo" }
      ]}
      associatedHref="#"
    />
  )
}
