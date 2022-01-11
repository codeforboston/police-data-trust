import { AccessToken, LoginCredentials, NewUser, ResetPasswordRequest, User } from ".."
import { EXISTING_TEST_USER, TestUser } from "./data"

export default class FakeAuth {
  users: TestUser[] = [EXISTING_TEST_USER]
  sessions: Record<AccessToken, TestUser> = {}
  sessionId = 1

  login({ email, password }: LoginCredentials): AccessToken | undefined {
    const user = this.users.find((u) => u.email === email && u.password === password)

    if (user) {
      const token = String(this.sessionId++)
      this.sessions[token] = user
      return token
    }
  }

  register(newUser: NewUser): AccessToken | undefined {
    if (this.users.some((u) => u.email === newUser.email)) {
      return
    }

    this.users.push({
      ...newUser,
      emailConfirmedAt: null,
      active: true,
      role: "Public"
    })

    return this.login(newUser)
  }

  forgot(email: string): void {
    // in the real API, this is secure because the token is sent to the registered email
    const user = this.users.find((u) => u.email === email)

    if (user) {
      const token = String(this.sessionId++)
      this.sessions[token] = user
    }
  }

  reset(request: ResetPasswordRequest): String | undefined {
    const { password, accessToken } = request
    const user = this.sessions[accessToken]

    if (user) {
      user.password = password
      return "Password reset successfully"
    } else {
      throw new Error("Missing JWT in headers or cookies")
    }
  }

  whoami(token: AccessToken): User | undefined {
    return this.sessions[token]
  }
}
