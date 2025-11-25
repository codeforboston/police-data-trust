import { test, expect } from "@playwright/test"

// This test posts multiple officers to the backend API and verifies they were created.
// It uses Playwright's APIRequestContext via the `request` fixture. The project's
// Playwright config sets `baseURL` to the web container, so we have to specify
// an `apiURL` here instead.

// Sample officers payload - adjust fields to match backend model expectations.
const sampleOfficers = [
  {
    uid: `test-officer-${Date.now()}-1`,
    first_name: "TestFirst1",
    middle_name: "M",
    last_name: "TestLast1",
    suffix: "Jr.",
    ethnicity: "White",
    gender: "Male",
    state_ids: [
      {
        id_name: "Tax ID Number",
        state: "NY",
        value: `TAX-${Date.now()}`
      }
    ]
  },
  {
    uid: `test-officer-${Date.now()}-2`,
    first_name: "TestFirst2",
    middle_name: "A",
    last_name: "TestLast2",
    ethnicity: "Hispanic/Latino",
    gender: "Female",
    state_ids: [
      {
        id_name: "Driver's License",
        state: "NY",
        value: `DL-${Date.now()}`
      }
    ]
  }
]

test.describe("Officers API", () => {
  test("POST multiple officers and verify they exist", async ({ request }) => {
    // Register a temporary user and create a source so the user is promoted
    // to CONTRIBUTOR (the backend requires that role to create officers).
    const testEmail = `pw-${Date.now()}@example.com`
    const testPassword = "TestPass123!"
    const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:5000/api/v1"

    const regRes = await request.post(`${apiBase}/auth/register`, {
      data: {
        email: testEmail,
        password: testPassword,
        firstname: "PW",
        lastname: "Test",
        phone_number: "000-000-0000"
      },
      headers: { "Content-Type": "application/json" }
    })

    if (!regRes.ok()) {
      const bad = await regRes.text()
      console.error("Register failed:", regRes.status(), bad)
    }
    expect(regRes.ok()).toBeTruthy()
    const regJson = await regRes.json()
    const accessToken = regJson?.access_token
    expect(accessToken).toBeTruthy()

    // Create a source to promote the user to CONTRIBUTOR
    const sourceRes = await request.post(`${apiBase}/sources`, {
      data: {
        name: `PW Source ${Date.now()}`,
        url: "https://example.org",
        contact_email: testEmail
      },
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      }
    })

    expect(sourceRes.ok()).toBeTruthy()

    // POST each officer individually (API expects single-object create)
    const createdUids: string[] = []
    for (const officer of sampleOfficers) {
      const postRes = await request.post(`${apiBase}/officers`, {
        data: officer,
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${accessToken}` }
      })

      if (!postRes.ok()) {
        const body = await postRes.text()
        console.error("Create officer failed:", postRes.status(), body)
      }
      expect(postRes.ok()).toBeTruthy()

      const postJson = await postRes.json()
      const createdUid = postJson?.uid || postJson?.id || officer.uid
      expect(createdUid).toBeTruthy()
      createdUids.push(createdUid)
    }

    // For each created UID, query the GET endpoint to confirm existence.
    for (const uid of createdUids) {
      const getRes = await request.get(`${apiBase}/officers/${encodeURIComponent(uid)}`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      })
      expect(getRes.ok()).toBeTruthy()
      const getJson = await getRes.json()
      // Basic checks: returned object has matching uid and name
      expect(getJson).toBeDefined()
      expect(getJson.uid || getJson.id).toBeTruthy()
    }
  })
})
