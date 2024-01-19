import { EmploymentType } from "../../../../models/officer"
import styles from "./work-history-instance.module.css"
import Image from "next/image"

export default function WorkHistoryInstance(pastWorkplace: EmploymentType) {
  const { agency, currentlyEmployed, earliestEmployment, latestEmployment } = pastWorkplace
  const { agencyName, agencyImage, agencyHqAddress, websiteUrl } = agency
  const startDateString = earliestEmployment.toLocaleDateString().split("/")[2]
  const endDateString = latestEmployment.toLocaleDateString().split("/")[2]

  const { patch, wrapper, titleAndDate, title, address, content, link } = styles

  return (
    <div className={wrapper}>
      <img className={patch} src={agencyImage} alt={agencyName.concat(" Patch")} />
      <div className={content}>
        <div className={titleAndDate}>
          <span className={title}>Detective</span>
          <span>
            {startDateString} - {endDateString}
          </span>
        </div>
        <a href={websiteUrl} className={link}>
          {agencyName}
        </a>
        {/*TODO: Get Phone number from officer data, mock data currently does not have*/}
        <p className={address}>(123) 456-7890 * {agencyHqAddress}</p>
      </div>
    </div>
  )
}
