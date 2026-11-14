 
import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
 
export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
 
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
 
  function handleSubmit(e) {
    e.preventDefault();
 
    if (!email.trim() || !password) {
      setError("Enter your email and password.");
      return;
    }
 
    login(email.trim());
 
    const destination = location.state?.from?.pathname || "/payment";
    navigate(destination, { replace: true });
  }
 
  return (
    <main className="form-container">
      <form className="form-card" onSubmit={handleSubmit}>
        <h1>Sign in</h1>
        <p>Sign in to continue with your order.</p>
 
        <label>Email address</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          required
        />
 
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter a demo password"
          required
        />
 
        {error && <p className="error">{error}</p>}
 
        <button type="submit">Sign in</button>
 
        <p className="muted">
          Demo only: any non-empty password is accepted.
        </p>
 
        <Link to="/">Back to shopping</Link>
      </form>
    </main>
  );
}
 