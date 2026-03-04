import ContentDetails from "./ContentDetails"
import { Officer } from "@/utils/api"

type OfficerContentDetailsProps = {
  officer: Officer
}

export default function OfficerContentDetails({ officer }: OfficerContentDetailsProps) {
  const totalComplaints =
    officer.allegation_summary?.reduce((sum, a) => sum + a.complaint_count, 0) || 0

  const totalAllegations =
    officer.allegation_summary?.reduce((sum, a) => sum + a.count, 0) || 0

  const totalSubstantiated =
    officer.allegation_summary?.reduce((sum, a) => sum + a.substantiated_count, 0) || 0

  const dataSources =
    officer.sources
      ?.map((source) => source.name)
      .filter((name): name is string => Boolean(name)) || []

  return (
    <ContentDetails
      contentType="Officer"
      dataSources={dataSources}
      lastUpdatedText="Nov 1, 2024 by"
      lastUpdatedBy="Adam Zelitzky"
      summaryItems={[
        { label: "Complaints", value: String(totalComplaints) },
        { label: "Allegations", value: String(totalAllegations) },
        { label: "Substantiated", value: String(totalSubstantiated) },
        { label: "Awards", value: "0" },
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