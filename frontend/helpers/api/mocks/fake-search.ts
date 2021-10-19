import { Incident, IncidentSearchRequest, IncidentSearchResponse } from ".."
import { EXISTING_TEST_INCIDENTS } from "./data"

export default class FakeSearch {
  incidents: Incident[] = EXISTING_TEST_INCIDENTS

  search({
    location,
    description,
    endTime,
    startTime,
    page = 1,
    perPage = 20
  }: IncidentSearchRequest): IncidentSearchResponse {
    const end = endTime && new Date(endTime)
    const start = startTime && new Date(startTime)
    const results = EXISTING_TEST_INCIDENTS.filter(
      (i) => !location || i.location?.toLowerCase()?.includes(location.toLowerCase())
    )
      .filter(
        (i) => !description || i.description?.toLowerCase()?.includes(description.toLowerCase())
      )
      .filter((i) => {
        const t = i.time_of_incident && new Date(i.time_of_incident)
        if (!end && !start) {
          return true
        } else if (!t) {
          return false
        } else {
          return (!end || t <= end) && (!start || t >= start)
        }
      })
    const resultStart = perPage * (page - 1),
      resultEnd = resultStart + perPage
    const pagedResults = results.slice(resultStart, resultEnd)
    return {
      results: pagedResults,
      totalResults: results.length,
      page: page,
      totalPages: Math.ceil(results.length / perPage)
    }
  }
}
