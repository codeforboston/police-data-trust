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
    const converted: EmploymentType[] = workHistory.map((item) => {
      return {
        department: {
          departmentName: item.deptName,
          deptImage: item.deptImage.replace("./frontend/models/mock-data/dept-images", ""),
          deptAddress: item.deptAddress,
          webAddress: "https://www.google.com/search?q=police+department"
        },
        status: item.status,
        startDate: new Date(item.dates.split("-")[0].trim()),
        endDate: new Date(item.dates.split("-")[1].trim())
      }
    })
    return converted
  }

  function mockToIncidentType(incidents: typeof officer.incidents): Incident[] {
    const officerNames = incidents[0].officers
    function mockToOfficerNameType(names: typeof officerNames): Officer[] {
      const converted: Officer[] = names.map((item) => {
        return {
          first_name: item.split(".")[0] + ".",
          last_name: item.split(".")[1]
        }
      })
      return converted
    }

    const usesOfForce = incidents[0].useOfForce
    function mockToForceType(forces: typeof usesOfForce): UseOfForce[] {
      const converted: UseOfForce[] = forces.map((force) => {
        return {
          item: force
        }
      })
      return converted
    }

    const converted: Incident[] = incidents.map((incident) => {
      return {
        ...incident,
        id: incident.id,
        officers: mockToOfficerNameType(incident.officers),
        use_of_force: mockToForceType(incident.useOfForce)
      }
    })
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
