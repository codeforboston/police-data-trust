import { EmploymentType } from "../../../../models/officer"
import styles from "./work-history-instance.module.css"
import Image from "next/image"

export default function WorkHistoryInstance(pastWorkplace: EmploymentType) {
  const { agency, status, startDate, endDate } = pastWorkplace
  const { agencyName, deptImage, agencyHqAddress, webAddress } = agency
  const startDateString = new Date(startDate).toLocaleDateString().split(",")[0]
  const endDateString = new Date(endDate).toLocaleDateString().split(",")[0]

  const { patch, wrapper, dates } = styles

  return (
    <div className={wrapper}>
      <img className={patch} src={deptImage} alt={agencyName.concat(" Patch")} />
      <div>
        <p>
          {status}
          <span className={dates}>
            {startDateString} - {endDateString}
          </span>
        </p>
        <a href={webAddress}>{agencyName}</a>
        {/*TODO: Get Phone number from officer data, mock data currently does not have*/}
        <p>(123) 456-7890 * {agencyHqAddress}</p>
      </div>
    </div>
  )
}
