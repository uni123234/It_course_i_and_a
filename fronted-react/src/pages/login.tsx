import '../styles/Login.css'

function LoginPage() {

  return (
    <div className='login-page'>
        <div className="container">
            <div className="image-section"></div>
            <div className="form-section">
                <div className="form-container">
                    <h2>Welcome Back!</h2>
                    <form>
                        <label htmlFor="email">Email Address</label>
                        <input type="email" id="email" name="email" placeholder="example@mail.com" />
                        {/* <p *ngIf="loginForm.submitted && emailInvalid">Please write the correct email.</p> */}
                        <label htmlFor="password">Password</label>
                        <input type="password" id="password" name="password" placeholder="********" />
                        {/* <p *ngIf="loginForm.submitted && passwordInvalid">Password must be at least 6 characters long.</p> */}
                        <button type="submit">Login</button>
                        {/* <p *ngIf="credentialsError">{{ credentialsError }}</p> */}
                        <div className="signup-link">
                            Don't have an account yet? <a href="/register">Create an account</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
  )
}

export default LoginPage
