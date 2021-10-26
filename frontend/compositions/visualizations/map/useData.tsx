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

  const addStateCode = () => {
    const idToStateNumber = Math.floor(Math.random() * 51)
    const stateCode = idToStateNumber < 10 ? "0" + idToStateNumber : idToStateNumber.toString()
    return stateCode
  }

  const fakeData = incidents.map((i) => {
    const stateCode = addStateCode()
    return { ...i, state: stateCode, value: i.officers.length } as FakeData
  })

  return fakeData
}
