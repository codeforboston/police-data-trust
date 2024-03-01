import axiosModule, { AxiosRequestConfig } from "axios"
import { baseURL } from "./config"

export type AccessToken = string

export interface AuthenticatedRequest {
  accessToken: AccessToken
}

const axios = axiosModule.create({
  baseURL,
  timeout: 5000
})

export function request({
  accessToken,
  ...config
}: AxiosRequestConfig & { accessToken?: AccessToken }) {
  let { headers, ...rest } = config
  if (accessToken) {
    headers = {
      Authorization: `Bearer ${accessToken}`,
      ...headers
    }
  }

  return axios({
    headers,
    ...rest
  }).then((response) => response.data)
}
