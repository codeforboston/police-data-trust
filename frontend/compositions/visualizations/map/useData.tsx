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

  let nextStateNumber = 0
  const addStateCode = () => {
    const stateNumber = (nextStateNumber++ % 50) + 1; 
    const stateCode = stateNumber < 10 ? "0" + stateNumber : stateNumber.toString()
    return stateCode
  }

  const fakeData = incidents.map((i) => {
    const stateCode = addStateCode()
    return { ...i, state: stateCode, value: i.officers.length } as FakeData
  })

  return fakeData
}
