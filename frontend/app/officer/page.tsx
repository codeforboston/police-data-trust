"use client"

import React, { useEffect, useState } from "react"
import API_ROUTES, { apiBaseUrl } from "@/utils/apiRoutes"
import { apiFetch } from "@/utils/apiFetch"
import { useSearchParams } from "next/navigation"
import { Avatar, Card, CardContent } from "@mui/material"
import styles from "./page.module.css"

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
    return <div style={{ padding: "16px" }}>No officer UID provided.</div>
  }

  if (loading) {
    return <div style={{ padding: "16px" }}>Loading officer details...</div>
  }

  if (error) {
    return <div style={{ padding: "16px", color: "#d32f2f" }}>Error: {error}</div>
  }

  if (!officer) {
    return <div style={{ padding: "16px" }}>Officer not found.</div>
  }

  const fullName = [officer.first_name, officer.middle_name, officer.last_name, officer.suffix]
    .filter(Boolean)
    .join(" ")

  const totalAllegations = officer.allegation_summary.reduce((sum, item) => sum + item.count, 0)
  const totalSubstantiated = officer.allegation_summary.reduce(
    (sum, item) => sum + item.substantiated_count,
    0
  )

  const primaryEmployment = officer.employment_history[0]

  return (
    <div className={styles.container}>
      {/* Header Section */}
      <Card variant="outlined">
        <CardContent sx={{ p: "32px" }}>
          <div className={styles.header}>
            <Avatar className={styles.avatar} />
            <div className={styles.headerInfo}>
              <h1>{fullName}</h1>
              <p>
                {officer.ethnicity} {officer.gender.toLowerCase()}
              </p>
              {primaryEmployment && (
                <p>
                  {primaryEmployment.highest_rank} at {primaryEmployment.agency_name}
                  {primaryEmployment.unit_name && `, ${primaryEmployment.unit_name}`}
                </p>
              )}
              {primaryEmployment?.salary && (
                <p>Earned ${primaryEmployment.salary.toLocaleString()} last year</p>
              )}
              {primaryEmployment?.badge_number && <p>Badge #{primaryEmployment.badge_number}</p>}
              {officer.state_ids && officer.state_ids.length > 0 && (
                <p>
                  {officer.state_ids[0].state} Driver's License {officer.state_ids[0].value}
                </p>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tab Navigation */}
      <Card variant="outlined" sx={{ mt: "16px", mb: 0 }}>
        <div className={styles.tabs}>
          <button className={`${styles.tab} ${styles.active}`}>Background</button>
          <button className={styles.tab}>Complaints</button>
          <button className={styles.tab}>Lawsuits</button>
        </div>
      </Card>

      {/* Main Content Area */}
      <div className={styles.mainContent}>
        {/* Left Column - Main Content */}
        <div className={styles.leftColumn}>
          <Card variant="outlined">
            <CardContent sx={{ p: "24px", pb: "32px" }}>
              <h2 className={styles.sectionTitle}>Background</h2>

              {/* State Records */}
              {officer.state_ids && officer.state_ids.length > 0 && (
                <div style={{ marginBottom: "24px" }}>
                  <h3 className={styles.subsectionTitle}>State records</h3>
                  {officer.state_ids.map((id, index) => (
                    <div key={index} className={styles.stateRecord}>
                      {id.state === "NY" ? "New York" : id.state} Driver's License, {id.state}-
                      {id.value}, 2023 - present
                    </div>
                  ))}
                </div>
              )}

              {/* Employment Records */}
              {officer.employment_history && officer.employment_history.length > 0 && (
                <div>
                  <h3 className={styles.subsectionTitle}>Employment records</h3>
                  {officer.employment_history.map((employment, index) => (
                    <div key={index} className={styles.employmentRecord}>
                      <div className={styles.employmentDate}>
                        {new Date(employment.earliest_date).toLocaleDateString("en-US", {
                          month: "short",
                          year: "numeric"
                        })}{" "}
                        -{" "}
                        {employment.latest_date
                          ? new Date(employment.latest_date).toLocaleDateString("en-US", {
                              month: "short",
                              year: "numeric"
                            })
                          : "present"}
                      </div>
                      <div className={styles.employmentDetails}>
                        <div className={styles.employmentBullet} />
                        <div className={styles.employmentInfo}>
                          <div className={styles.employmentRank}>{employment.highest_rank}</div>
                          <div className={styles.employmentAgency}>
                            {employment.agency_name}
                            {employment.unit_name && `, ${employment.unit_name}`}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Allegations Section */}
          {officer.allegation_summary && officer.allegation_summary.length > 0 && (
            <Card variant="outlined" sx={{ mt: "16px" }}>
              <CardContent sx={{ p: "24px" }}>
                <div className={styles.allegationsHeader}>
                  <div>
                    <span className={styles.allegationsTitle}>Allegations</span>
                    <span className={styles.allegationsMeta}>
                      {totalAllegations} complaints • {totalAllegations} Allegations •{" "}
                      {totalSubstantiated} Substantiated
                    </span>
                  </div>
                  <button className={styles.viewAllButton}>View all</button>
                </div>
                <div>
                  {officer.allegation_summary.map((allegation, index) => (
                    <div key={index} className={styles.allegationItem}>
                      <div className={styles.allegationType}>{allegation.type}</div>
                      <div className={styles.allegationDetails}>
                        {allegation.count} complaints, {allegation.substantiated_count}{" "}
                        substantiated, {allegation.earliest_incident_date.split("-")[0]} -{" "}
                        {allegation.latest_incident_date.split("-")[0]}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Right Sidebar */}
        <div className={styles.sidebar}>
          <Card variant="outlined" sx={{ position: "sticky", top: "24px" }}>
            <CardContent sx={{ p: "20px" }}>
              <h3 className={styles.sidebarTitle}>Content Details</h3>

              <div className={styles.detailsLabel}>Content type</div>
              <div className={styles.detailsValue}>Officer</div>

              <div className={styles.detailsLabel}>Data sources</div>
              <div className={styles.detailsValue}>N/A</div>

              <div className={styles.detailsLabel}>Last updated</div>
              <div className={styles.detailsValue}>
                {new Date().toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric"
                })}
              </div>

              <div className={styles.detailsLabel}>Summary</div>
              <div className={styles.detailsValue}>
                <div style={{ marginBottom: "4px" }}>{totalAllegations} Complaints</div>
                <div style={{ marginBottom: "4px" }}>{totalAllegations} Allegations</div>
                <div style={{ marginBottom: "4px" }}>{totalSubstantiated} Substantiated</div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
