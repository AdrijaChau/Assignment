import { useCart } from "../context/CartContext";
import formatCurrency from "../utils/formatCurrency";
 
export default function ProductCard({ product }) {
  const { addToCart } = useCart();
 
  return (
    <article className="product-card">
      <img src={product.image} alt={product.name} />
      <p className="category">{product.category}</p>
      <h3>{product.name}</h3>
      <strong>{formatCurrency(product.price)}</strong>
      <p className="delivery-note">
        FREE delivery on orders over ₹999
      </p>
      <button onClick={() => addToCart(product)}>
        Add to Cart
      </button>
    </article>
  );
}