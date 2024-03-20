import { AccessToken, request } from "../base"
import { Incident, IncidentSearchRequest, IncidentSearchResponse } from "./types"

export function searchIncidents({
  accessToken,
  dateStart,
  dateEnd,
  ...rest
}: IncidentSearchRequest): Promise<IncidentSearchResponse> {
  if (dateStart) dateStart = new Date(dateStart).toISOString().slice(0, -1)
  if (dateEnd) dateEnd = new Date(dateEnd).toISOString().slice(0, -1)

  return request({
    url: "/incidents/search",
    method: "POST",
    accessToken,
    data: { dateStart, dateEnd, ...rest }
  })
}

export async function getIncidentById(id: number, accessToken: AccessToken): Promise<Incident> {
  return request({
    url: `/incidents/get/${id}`,
    method: "GET",
    accessToken
  })
}
