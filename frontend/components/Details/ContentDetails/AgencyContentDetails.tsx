import ContentDetails from "./ContentDetails"
import { Agency } from "@/utils/api"

type AgencyContentDetailsProps = {
  agency: Agency
}

const toOrganizationSlug = (name: string) =>
  name
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(".", "-")
    .replace(/[^a-z0-9-]/g, "")

export default function AgencyContentDetails({ agency }: AgencyContentDetailsProps) {
  const totalComplaints = agency.total_complaints || 0

  const totalOfficers = agency.total_officers || 0

  const dataSources =
    agency.sources
      ?.filter((source): source is { name: string; uid?: string } => Boolean(source.name))
      .map((source) => ({
        label: source.name,
        href: `/organization?slug=${toOrganizationSlug(source.name)}`
      })) || []

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
