import React from 'react';
import ProductCard from './components/ProductCard';

const products = [
  { id: 1, name: 'Венти', price: 1490, image: '/images/venti.png' },
  { id: 2, name: 'Арлекино', price: 1690, image: '/images/arlecchino.png' },
  { id: 3, name: 'Колокольный зверь', price: 1890, image: '/images/plush-3.png' },
  { id: 4, name: 'Айзек', price: 1390, image: '/images/isaac.png' },
  { id: 5, name: 'Макима', price: 990, image: '/images/makima.png' },
];

export default function App() {
  return (
    <main className="store">
      <h1>Neko <span>Plush</span></h1>
      <div className="product-grid">
        {products.map((product) => (
          <ProductCard key={product.id} name={product.name} price={product.price} image={product.image} />
        ))}
      </div>
    </main>
  );
}
