import { Incident, User } from ".."

export type TestUser = User & { password: string }

/** Matches alembic/dev_seeds.py */
export const EXISTING_TEST_USER: TestUser = {
  active: true,
  emailConfirmedAt: null,
  email: "test@example.com",
  password: "password",
  firstName: "Test",
  lastName: "Example",
  phoneNumber: "(123) 456-7890",
  role: "Public"
}

/** Matches alembic/dev_seeds.py */
export const EXISTING_TEST_INCIDENTS: Incident[] = (
  [
    [1, "10-01-2019Z"],
    [2, "11-01-2019Z"],
    [3, "12-01-2019Z"],
    [4, "03-15-2020Z"],
    [5, "04-15-2020Z"],
    [6, "08-10-2020Z"],
    [7, "10-01-2020Z"],
    [8, "10-15-2020Z"]
  ] as const
).map(([key, date]) => createTestIncident(key, date))

function createTestIncident(key: number, date: string) {
  const baseId = 10000000
  return {
    id: baseId + key,
    department: `Small Police Department ${key}`,
    description: `Test description ${key}`,
    location: `Test location ${key}`,
    officers: [
      {
        first_name: `TestFirstName ${key}`,
        last_name: `TestLastName ${key}`
      }
    ],
    source: "mpv",
    time_of_incident: new Date(date).toUTCString(),
    use_of_force: [
      {
        item: `gunshot ${key}`
      }
    ]
  }
}
