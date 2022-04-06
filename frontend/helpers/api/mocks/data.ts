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
    [1, "10-01-2019Z", [-87.6974962, 41.6928005]],
    [2, "11-01-2019Z", [-87.6621781, 41.7511912]],
    [3, "12-01-2019Z", [-87.628557, 41.751667]],
    [4, "03-15-2020Z", [-87.5667172, 41.7642916]],
    [5, "04-15-2020Z", [-87.7690689, 41.7932642]],
    [6, "08-10-2020Z", [-87.6073355, 41.8060329]],
    [7, "10-01-2020Z", [-87.6958407, 41.8125757]],
    [8, "10-15-2020Z", [-87.6951311, 41.8190785]]
  ] as const
).map(([key, date, lonlat]) => createTestIncident(key, date, lonlat))

function createTestIncident(
  key: number,
  date: string,
  lonlat: readonly [number, number]
): Incident {
  const baseId = 10000000
  return {
    id: baseId + key,
    department: `Small Police Department ${key}`,
    description: `Test description ${key}`,
    location: `Test location ${key}`,
    locationLonLat: [lonlat[0], lonlat[1]],
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
