import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import formatCurrency from "../utils/formatCurrency";
 
export default function Cart() {
  const {
    cart, removeFromCart, updateQuantity,
    subtotal, delivery, total,
  } = useCart();
 
  const navigate = useNavigate();
 
  return (
    <main className="container">
      <h1>Your Shopping Cart</h1>
 
      {cart.length === 0 ? (
        <section className="empty-state">
          <h2>Your cart is empty</h2>
          <p>Add products to get started.</p>
          <Link to="/">Continue shopping</Link>
        </section>
      ) : (
        <div className="cart-layout">
          <section className="cart-list">
            {cart.map((item) => (
              <article className="cart-item" key={item.id}>
                <img src={item.image} alt={item.name} />
 
                <div className="cart-details">
                  <h3>{item.name}</h3>
                  <p className="stock">In stock</p>
                  <strong>{formatCurrency(item.price)}</strong>
 
                  <div className="quantity">
                    <button onClick={() =>
                      updateQuantity(item.id, item.quantity - 1)
                    }>−</button>
 
                    <span>{item.quantity}</span>
 
                    <button onClick={() =>
                      updateQuantity(item.id, item.quantity + 1)
                    }>+</button>
 
                    <button className="remove-btn" onClick={() =>
                      removeFromCart(item.id)
                    }>Remove</button>
                  </div>
                </div>
              </article>
            ))}
          </section>
 
          <aside className="summary">
            <h2>Order Summary</h2>
            <p><span>Subtotal</span><strong>{formatCurrency(subtotal)}</strong></p>
            <p><span>Delivery</span><strong>{delivery === 0 ? "FREE" : formatCurrency(delivery)}</strong></p>
            <hr />
            <h3>Total: {formatCurrency(total)}</h3>
 
            <button onClick={() => navigate("/payment")}>
              Proceed to Payment
            </button>
          </aside>
        </div>
      )}
    </main>
  );
}