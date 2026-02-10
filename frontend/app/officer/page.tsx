"use client"

import React, { useEffect, useState } from "react"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { apiFetch } from "@/utils/apiFetch"
import { useSearchParams } from "next/navigation"

interface StateId {
  id_name: string
  state: string
  value: string
}

interface EmploymentHistory {
  earliest_date: string
  badge_number: string
  highest_rank: string
  latest_date: string | null
  salary: number | null
  unit_name: string
  agency_name: string
  agency_uid: string
  unit_uid: string
}

interface AllegationSummary {
  type: string
  count: number
  substantiated_count: number
  earliest_incident_date: string
  latest_incident_date: string
}

interface OfficerData {
  uid: string
  first_name: string
  middle_name: string | null
  last_name: string
  suffix: string | null
  ethnicity: string
  gender: string
  state_ids: StateId[]
  employment_history: EmploymentHistory[]
  allegation_summary: AllegationSummary[]
}

export default function OfficerDetailsPage() {
  const searchParams = useSearchParams()
  const uid = searchParams.get("uid")
  const [officer, setOfficer] = useState<OfficerData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchOfficerDetails = async () => {
      if (!uid) {
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        const response = await apiFetch(
          `${apiBaseUrl}${API_ROUTES.search.officers}${uid}?include=allegations&include=employment`
        )

        if (!response.ok) {
          throw new Error(`Failed to fetch officer details: ${response.statusText}`)
        }

        const data = await response.json()
        setOfficer(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred")
      } finally {
        setLoading(false)
      }
    }

    fetchOfficerDetails()
  }, [uid])

  if (!uid) {
    return <div className="p-4">No officer UID provided.</div>
  }

  if (loading) {
    return <div className="p-4">Loading officer details...</div>
  }

  if (error) {
    return <div className="p-4 text-red-600">Error: {error}</div>
  }

  if (!officer) {
    return <div className="p-4">Officer not found.</div>
  }

  const fullName = [
    officer.first_name,
    officer.middle_name,
    officer.last_name,
    officer.suffix
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <div className="container mx-auto p-4 max-w-6xl">
      <h1 className="text-3xl font-bold mb-6">Officer Details</h1>

      <div className="space-y-6">
        {/* Basic Information */}
        <section className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Basic Information</h2>
          <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <dt className="text-sm font-medium text-gray-500">Name</dt>
              <dd className="mt-1 text-lg font-semibold">{fullName}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Gender</dt>
              <dd className="mt-1">{officer.gender}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Ethnicity</dt>
              <dd className="mt-1">{officer.ethnicity}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Officer ID</dt>
              <dd className="mt-1 text-sm font-mono">{officer.uid}</dd>
            </div>
          </dl>

          {officer.state_ids && officer.state_ids.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium mb-3">State IDs</h3>
              <div className="space-y-2">
                {officer.state_ids.map((id, index) => (
                  <div key={index} className="flex items-center space-x-4 bg-gray-50 p-3 rounded">
                    <span className="font-medium">{id.id_name}:</span>
                    <span>{id.value}</span>
                    <span className="text-sm text-gray-500">({id.state})</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* Employment History */}
        {officer.employment_history && officer.employment_history.length > 0 && (
          <section className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Employment History</h2>
            <div className="space-y-4">
              {officer.employment_history.map((employment, index) => (
                <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                  <h3 className="font-semibold text-lg">{employment.agency_name}</h3>
                  <div className="mt-2 space-y-1 text-sm">
                    <p>
                      <span className="font-medium">Unit:</span> {employment.unit_name}
                    </p>
                    <p>
                      <span className="font-medium">Rank:</span> {employment.highest_rank}
                    </p>
                    <p>
                      <span className="font-medium">Badge:</span> {employment.badge_number}
                    </p>
                    <p>
                      <span className="font-medium">Period:</span>{" "}
                      {new Date(employment.earliest_date).toLocaleDateString()} -{" "}
                      {employment.latest_date
                        ? new Date(employment.latest_date).toLocaleDateString()
                        : "Present"}
                    </p>
                    {employment.salary && (
                      <p>
                        <span className="font-medium">Salary:</span> $
                        {employment.salary.toLocaleString()}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Allegation Summary */}
        {officer.allegation_summary && officer.allegation_summary.length > 0 && (
          <section className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Allegation Summary</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Total
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Substantiated
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date Range
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {officer.allegation_summary.map((allegation, index) => (
                    <tr key={index} className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                      <td className="px-6 py-4 whitespace-nowrap font-medium">
                        {allegation.type}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">{allegation.count}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-red-600 font-semibold">
                          {allegation.substantiated_count}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(allegation.earliest_incident_date).toLocaleDateString()} -{" "}
                        {new Date(allegation.latest_incident_date).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </div>
    </div>
  )
}
