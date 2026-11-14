import { Link, Navigate, useLocation } from "react-router-dom";
import formatCurrency from "../utils/formatCurrency";
 
export default function OrderSuccess() {
  const { state } = useLocation();
  const order = state?.order;
 
  if (!order) {
    return <Navigate to="/" replace />;
  }
 
  return (
    <main className="container success-page">
      <div className="success-icon">✓</div>
      <h1>Order placed successfully!</h1>
      <p>Thank you, {order.customer}.</p>
      <p>Order ID: <strong>{order.id}</strong></p>
 
      <section className="summary">
        <h2>Order details</h2>
 
        {order.items.map((item) => (
          <p key={item.id}>
            {item.name} × {item.quantity}
            {" — "}
            {formatCurrency(item.price * item.quantity)}
          </p>
        ))}
 
        <h3>Total: {formatCurrency(order.total)}</h3>
        <p className="stock">Demo payment successful</p>
      </section>
 
      <p className="muted">
        No money was charged. This is a simulated order.
      </p>
 
      <Link to="/">Continue shopping</Link>
    </main>
  );
}