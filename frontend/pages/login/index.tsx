export default function Login() {
  return (
    <div className="Login">
      <img src="" placeholder="login logo" />
      <h1>Login</h1>
      <article className="email-container">
        <label htmlFor="email">Email:</label>
        <input name="email" type="text" placeholder="Email" />
      </article>
      <article className="password-container">
        <label htmlFor="password">Password:</label>
        <input name="password" type="password" placeholder="something" />
      </article>
    </div>
  )
}
