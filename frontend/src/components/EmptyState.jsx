// Estado vacio reutilizable con accion principal.
import React from 'react';

export default function EmptyState({ icono, imagen, titulo, texto, accion }) {
  return (
    <div className="empty-state">
      {imagen ? (
        <img className="empty-ilustracion" src={imagen} alt="" aria-hidden="true" />
      ) : (
        <div className="empty-icon" aria-hidden="true">{icono}</div>
      )}
      <h3>{titulo}</h3>
      <p>{texto}</p>
      {accion}
    </div>
  );
}
