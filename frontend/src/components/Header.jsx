// Header de la app: titulo de la pagina.
import React from 'react';

export default function Header({ titulo }) {
  return (
    <header className="topbar">
      <span>{titulo}</span>
    </header>
  );
}
