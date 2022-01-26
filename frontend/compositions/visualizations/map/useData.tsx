import { mockIncident as incidents } from "../../../models/mock-data"
import { PointCoord } from "../utilities/chartTypes"

type StateID = string

type FakeData = {
  UID?: number
  id?: number
  occurred?: number
  officers?: string[]
  incidentType?: string
  useOfForce?: string[]
  source?: string
  location?: PointCoord
  state?: StateID
  label?: string
  value?: number
}

export default function useData() {
  // using mock data set

  const stateArray = [
    16, 25, 7, 10, 8, 21, 24, 39, 40, 39, 18, 37, 28, 35, 15, 26, 22, 8, 2, 24, 5, 45, 22, 15, 6,
    49, 23, 22, 12, 14, 16, 1, 23, 36, 24, 42, 41, 15, 32, 47, 37, 4, 38, 49, 49, 9, 21, 6, 33, 44,
    29, 36, 44, 34, 29, 47, 36, 2, 44, 17, 24, 44, 38, 35, 24, 45, 5, 42, 48, 4, 24, 33, 4, 46, 13,
    40, 27, 29, 0, 31, 0, 1, 21, 34, 49, 39, 0, 1, 25, 14, 1, 18, 6, 8, 27, 9, 40, 43, 46, 43
  ]

  let nextStateNumber = 0
  const addStateCode = () => {
    const stateNumber = stateArray[nextStateNumber++]
    const stateCode = stateNumber < 10 ? "0" + stateNumber : stateNumber.toString()
    return stateCode
  }

  const fakeData = incidents.map((i) => {
    const stateCode = addStateCode()
    return { ...i, state: stateCode, value: i.officers.length } as FakeData
  })

  return fakeData
}
