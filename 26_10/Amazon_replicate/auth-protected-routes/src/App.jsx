 
import { BrowserRouter, Routes, Route } from "react-router-dom";
 
import { AuthProvider } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";
 
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
 
import Home from "./pages/Home";
import Login from "./pages/Login";
import Cart from "./pages/Cart";
import Payment from "./pages/Payment";
import OrderSuccess from "./pages/OrderSuccess";
 
import "./App.css";
 
export default function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <BrowserRouter>
          <Navbar />
 
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/cart" element={<Cart />} />
 
            <Route
              path="/payment"
              element={
                <ProtectedRoute>
                  <Payment />
                </ProtectedRoute>
              }
            />
 
            <Route
              path="/order-success"
              element={
                <ProtectedRoute>
                  <OrderSuccess />
                </ProtectedRoute>
              }
            />
 
            <Route path="*" element={<Home />} />
          </Routes>
        </BrowserRouter>
      </CartProvider>
    </AuthProvider>
  );
}
 
  
