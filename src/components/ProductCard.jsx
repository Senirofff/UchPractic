import React, { useState } from 'react';

export default function ProductCard({ name, price, image }) {
  const [quantity, setQuantity] = useState(0);

  function addToCart() {
    setQuantity((current) => current + 1);
  }

  return (
    <article className="product-card">
      <img src={image} alt={`Плюшевая игрушка «${name}»`} />
      <div className="product-info">
        <h2>{name}</h2>
        <p className="price">{price.toLocaleString('ru-RU')} ₽</p>
        <button onClick={addToCart} aria-label={`Добавить «${name}» в корзину`}>
          Добавить в корзину
        </button>
        <p className="quantity" aria-live="polite">Выбрано: {quantity}</p>
      </div>
    </article>
  );
}
