import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import formatCurrency from "../utils/formatCurrency";
 
export default function Payment() {
  const { cart, total, setCart } = useCart();
  const navigate = useNavigate();
 
  const [name, setName] = useState("Demo Customer");
  const [card, setCard] = useState("4242 4242 4242 4242");
  const [expiry, setExpiry] = useState("12/30");
  const [cvv, setCvv] = useState("123");
  const [error, setError] = useState("");
 
  function handlePayment(e) {
    e.preventDefault();
    setError("");
 
    if (cart.length === 0) {
      setError("Your cart is empty.");
      return;
    }
 
    if (!name.trim() || !/^\d{16}$/.test(card.replace(/\s/g, ""))) {
      setError("Enter a name and a 16-digit dummy card number.");
      return;
    }
 
    if (!/^\d{2}\/\d{2}$/.test(expiry) ||
        !/^\d{3,4}$/.test(cvv)) {
      setError("Enter expiry as MM/YY and a 3- or 4-digit CVV.");
      return;
    }
 
    const [month, year] = expiry.split("/").map(Number);
    const now = new Date();
    const currentYear = now.getFullYear() % 100;
    const currentMonth = now.getMonth() + 1;
 
    if (
      month < 1 || month > 12 ||
      year < currentYear ||
      (year === currentYear && month < currentMonth)
    ) {
      setError("Enter a valid future expiry date.");
      return;
    }
 
    const order = {
      id: "DEMO-" + Date.now().toString().slice(-8),
      items: cart.map((item) => ({ ...item })),
      total,
      customer: name.trim(),
    };
 
    setCart([]);
    navigate("/order-success", { state: { order } });
  }
 
  return (
    <main className="form-container">
      <form className="form-card payment-form" onSubmit={handlePayment}>
        <h1>Checkout & Payment</h1>
        <h2>Total: {formatCurrency(total)}</h2>
 
        <div className="demo-notice">
          <strong>Demo card details</strong>
          <p>Card: 4242 4242 4242 4242</p>
          <p>Expiry: 12/30</p>
          <p>CVV: 123</p>
          <button type="button" onClick={() => {
            setName("Demo Customer");
            setCard("4242 4242 4242 4242");
            setExpiry("12/30");
            setCvv("123");
          }}>
            Fill demo details
          </button>
        </div>
 
        <label>Name on card</label>
        <input value={name} onChange={(e) => setName(e.target.value)} required />
 
        <label>Dummy card number</label>
        <input
          value={card}
          onChange={(e) => {
            const digits = e.target.value.replace(/\D/g, "").slice(0, 16);
            setCard(digits.replace(/(\d{4})(?=\d)/g, "$1 "));
          }}
          inputMode="numeric"
          required
        />
 
        <label>Expiry (MM/YY)</label>
        <input value={expiry} onChange={(e) => setExpiry(e.target.value)} required />
 
        <label>CVV</label>
        <input
          value={cvv}
          onChange={(e) => setCvv(e.target.value.replace(/\D/g, "").slice(0, 4))}
          inputMode="numeric"
          required
        />
 
        {error && <p className="error">{error}</p>}
 
        <button type="submit">Pay {formatCurrency(total)}</button>
        <p className="muted">
          Educational demo only. No actual payment is processed.
        </p>
      </form>
    </main>
  );
}