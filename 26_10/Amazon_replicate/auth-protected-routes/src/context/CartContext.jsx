 
import { createContext, useContext, useState } from "react";
 
const CartContext = createContext();
 
export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);
 
  function addToCart(product) {
    setCart((items) => {
      const found = items.find((item) => item.id === product.id);
 
      if (found) {
        return items.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
 
      return [...items, { ...product, quantity: 1 }];
    });
  }
 
  function removeFromCart(id) {
    setCart((items) => items.filter((item) => item.id !== id));
  }
 
  function updateQuantity(id, quantity) {
    if (quantity < 1) {
      removeFromCart(id);
      return;
    }
 
    setCart((items) =>
      items.map((item) =>
        item.id === id ? { ...item, quantity } : item
      )
    );
  }
 
  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = cart.reduce(
    (sum, item) => sum + item.price * item.quantity, 0
  );
  const delivery = subtotal === 0 || subtotal >= 999 ? 0 : 49;
  const total = subtotal + delivery;
 
  return (
    <CartContext.Provider
      value={{
        cart, setCart, addToCart, removeFromCart,
        updateQuantity, cartCount, subtotal, delivery, total,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}
 
export function useCart() {
  return useContext(CartContext);
}
 