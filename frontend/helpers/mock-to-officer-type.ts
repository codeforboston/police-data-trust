import { OfficerRecordType, EmploymentType } from "../models/officer"
import { Incident, Officer, UseOfForce } from "../helpers/api"
import officers from "../models/mock-data/officer.json"

export function getOfficerFromMockData(officerId: number) {
  if (officerId >= 0 && officerId < 100) {
    return mockToOfficerType(officers[officerId])
  }
}

export function mockToOfficerType(officer: typeof officers[0]): OfficerRecordType {
  function mockToWorkHistoryType(workHistory: typeof officer.workHistory): EmploymentType[] {
    let converted: EmploymentType[] = []
    for (let workInstance of workHistory) {
      converted.push({
        department: {
          departmentName: workInstance.deptName,
          deptImage: workInstance.deptImage.replace("./frontend/models/mock-data/dept-images", ""),
          deptAddress: workInstance.deptAddress,
          webAddress: "https://www.google.com/search?q=police+department"
        },
        status: workInstance.status,
        startDate: new Date(workInstance.dates.split("-")[0].trim()),
        endDate: new Date(workInstance.dates.split("-")[1].trim())
      })
    }

    return converted
  }

  function mockToIncidentType(incidents: typeof officer.incidents): Incident[] {
    let converted: Incident[] = []

    let officerNames = incidents[0].officers
    function mockToOfficerNameType(names: typeof officerNames): Officer[] {
      let converted: Officer[] = []
      for (let name of names) {
        converted.push({
          first_name: name.split(".")[0] + ".",
          last_name: name.split(".")[1]
        })
      }
      return converted
    }

    let usesOfForce = incidents[0].useOfForce
    function mockToForceType(forces: typeof usesOfForce): UseOfForce[] {
      let converted: UseOfForce[] = []
      for (let force of forces) {
        converted.push({
          item: force
        })
      }
      return converted
    }

    for (let incidentInstance of incidents) {
      converted.push({
        id: incidentInstance.id,
        officers: mockToOfficerNameType(incidentInstance.officers),
        use_of_force: mockToForceType(incidentInstance.useOfForce)
      })
    }
    return converted
  }

  return {
    recordId: officer.id,
    firstName: officer.firstName,
    lastName: officer.lastName,
    badgeNo: officer.badgeNo,
    status: officer.status,
    department: officer.department,
    birthDate: new Date(officer.birthDate),
    gender: officer.gender,
    race: officer.race,
    ethnicity: officer.ethnicity,
    incomeBracket: officer.incomeBracket,
    workHistory: mockToWorkHistoryType(officer.workHistory),
    affiliations: officer.affiliations,
    incidents: mockToIncidentType(officer.incidents)
  }
}
