import { EmploymentType } from "../../../../models/officer"
import styles from "./work-history-instance.module.css"
import Image from "next/image"

export default function WorkHistoryInstance(pastWorkplace: EmploymentType) {
  const { agency, currentlyEmployed, earliestEmployment, latestEmployment } = pastWorkplace
  const { agencyName, agencyImage, agencyHqAddress, websiteUrl } = agency
  const startDateString = new Date(earliestEmployment).toLocaleDateString().split(",")[0]
  const endDateString = new Date(latestEmployment).toLocaleDateString().split(",")[0]

  const { patch, wrapper, dates } = styles

  return (
    <div className={wrapper}>
      <img className={patch} src={agencyImage} alt={agencyName.concat(" Patch")} />
      <div>
        <p>
          {status}
          <span className={dates}>
            {startDateString} - {endDateString}
          </span>
        </p>
        <a href={websiteUrl}>{agencyName}</a>
        {/*TODO: Get Phone number from officer data, mock data currently does not have*/}
        <p>(123) 456-7890 * {agencyHqAddress}</p>
      </div>
    </div>
  )
}
