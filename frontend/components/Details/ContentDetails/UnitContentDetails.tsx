import ContentDetails from "./ContentDetails"
import { Unit } from "@/utils/api"

type UnitContentDetailsProps = {
  unit: Unit
}

export default function UnitContentDetails({ unit }: UnitContentDetailsProps) {
  const totalComplaints =
    unit.total_complaints || 0

  const totalAllegations = unit.total_allegations || 0

  const totalOfficers = unit.total_officers || 0

  const dataSources =
    unit.sources?.map((source) => source.name).filter((name): name is string => Boolean(name)) ||
    []

  return (
    <ContentDetails
      contentType="Unit"
      dataSources={dataSources}
      lastUpdatedText="Nov 1, 2024 by"
      lastUpdatedBy="Adam Zelitzky"
      summaryItems={[
        { label: "Officers", value: String(totalOfficers) },
        { label: "Complaints", value: String(totalComplaints) },
        { label: "Allegations", value: String(totalAllegations) },
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
