import { EmploymentType } from "../../../../models/officer"
import styles from "./work-history-instance.module.css"
import Image from "next/image"

export default function WorkHistoryInstance(pastWorkplace: EmploymentType) {
  const { department, status, startDate, endDate } = pastWorkplace
  const { departmentName, deptImage, deptAddress, webAddress } = department
  const startDateString = new Date(startDate).toLocaleDateString().split(",")[0]
  const endDateString = new Date(endDate).toLocaleDateString().split(",")[0]

  const { patch, wrapper, dates } = styles

  return (
    <div className={wrapper}>
      <img className={patch} src={deptImage} alt={departmentName.concat(" Patch")} />
      <div>
        <p>
          {status}
          <span className={dates}>
            {startDateString} - {endDateString}
          </span>
        </p>
        <a href={webAddress}>{departmentName}</a>
        {/*TODO: Get Phone number from officer data, mock data currently does not have*/}
        <p>(123) 456-7890 * {deptAddress}</p>
      </div>
    </div>
  )
}
