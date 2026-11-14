import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
 
export default function Navbar() {
  const { cartCount } = useCart();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
 
  return (
    <>
      <nav className="navbar">
        <Link className="logo" to="/">amazon.in</Link>
 
        <form className="nav-search" onSubmit={(e) => {
          e.preventDefault();
          navigate("/?search=" + encodeURIComponent(e.currentTarget.search.value));
        }}>
          <input name="search" placeholder="Search products..." />
          <button type="submit">Search</button>
        </form>
 
        <Link to="/">Home</Link>
        <Link to="/cart">Cart ({cartCount})</Link>
 
        {user ? (
          <>
            <span>Hello, {user.email}</span>
            <button onClick={() => {
              logout();
              navigate("/");
            }}>Logout</button>
          </>
        ) : (
          <Link to="/login">Sign in</Link>
        )}
      </nav>
 
      <div className="subnav">
        Electronics · Fashion · Home & Kitchen · Everyday essentials
      </div>
    </>
  );
}