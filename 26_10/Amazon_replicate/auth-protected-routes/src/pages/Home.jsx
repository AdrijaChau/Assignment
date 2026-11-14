import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import products from "../data/products";
import ProductCard from "../components/ProductCard";
 
export default function Home() {
  const location = useLocation();
  const [search, setSearch] = useState(
    new URLSearchParams(location.search).get("search") || ""
  );
  const [category, setCategory] = useState("All");
 
  useEffect(() => {
    setSearch(new URLSearchParams(location.search).get("search") || "");
  }, [location.search]);
 
  const filteredProducts = products.filter((product) => {
    const matchesSearch =
      `${product.name} ${product.category}`
        .toLowerCase()
        .includes(search.toLowerCase());
 
    const matchesCategory =
      category === "All" || product.category === category;
 
    return matchesSearch && matchesCategory;
  });
 
  return (
    <main className="container">
      <section className="hero">
        <div>
          <p>EVERYDAY ESSENTIALS</p>
          <h1>Find something you'll love.</h1>
          <p>Great products at great prices.</p>
        </div>
      </section>
 
      <div className="home-heading">
        <h2>Discover products</h2>
 
        <input
          className="search-input"
          type="search"
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
 
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option>All</option>
          <option>Electronics</option>
          <option>Fashion</option>
          <option>Home</option>
        </select>
      </div>
 
      <section className="product-grid">
        {filteredProducts.length > 0 ? (
          filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))
        ) : (
          <p>No products found. Try another search.</p>
        )}
      </section>
    </main>
  );
}