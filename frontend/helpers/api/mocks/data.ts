import { User } from ".."

export type TestUser = User & { password: string }

/** Matches alembic/dev_seeds.py */
export const EXISTING_TEST_USER: TestUser = {
  active: true,
  emailConfirmedAt: null,
  email: "test@example.com",
  password: "password",
  firstName: "Test",
  lastName: "Example"
}
