import { OfficerRecordType, EmploymentType } from "../models/officer"
import { PerpetratorRecordType } from "../models/perpetrator"
import { Incident, Officer, UseOfForce } from "../helpers/api"
import officers from "../models/mock-data/officer.json"
import { IncidentRecordType } from "../models/incident"

export function getOfficerFromMockData(officerId: number) {
  if (officerId >= 0 && officerId < 100) {
    return mockToOfficerType(officers[officerId])
  }
}

export function getPerpetratorFromMockData(perpetratorId: number) {
  if (perpetratorId >= 0 && perpetratorId < 100) {
    return mockToPerpetratorType(officers[perpetratorId])
  }
}

export function mockToOfficerType(officer: typeof officers[0]): OfficerRecordType {
  function mockToWorkHistoryType(workHistory: typeof officer.workHistory): EmploymentType[] {
    const converted: EmploymentType[] = workHistory.map((item) => {
      return {
        agency: {
          agencyName: item.deptName,
          agencyImage: item.deptImage.replace("./frontend/models/mock-data/dept-images", ""),
          agencyHqAddress: item.deptAddress,
          websiteUrl: "https://www.google.com/search?q=police+department"
        },
        currentlyEmployed: true,
        earliestEmployment: new Date(item.dates.split("-")[0].trim()),
        latestEmployment: new Date(item.dates.split("-")[1].trim())
      }
    })
    return converted
  }

  return {
    recordId: officer.id,
    firstName: officer.firstName,
    lastName: officer.lastName,
    dateOfBirth: new Date(officer.birthDate),
    gender: officer.gender,
    race: officer.race,
    badgeNo: officer.badgeNo,
    status: officer.status,
    department: officer.department,
    ethnicity: officer.ethnicity,
    affiliations: officer.affiliations,
    workHistory: mockToWorkHistoryType(officer.workHistory),
    incidents: mockToIncidentType(officer.incidents)
  }
}

export function mockToPerpetratorType(officer: typeof officers[0]): PerpetratorRecordType {
  return {
    recordId: officer.id,
    firstName: officer.firstName,
    lastName: officer.lastName,
    gender: officer.gender,
    race: officer.race
  }
}

export function mockToIncidentType(data: IncidentRecordType[]): IncidentRecordType[] {
  return data
}
