// Estado vacio reutilizable con accion principal.
import React from 'react';

export default function EmptyState({ icono, titulo, texto, accion }) {
  return (
    <div className="empty-state">
      <div className="empty-icon" aria-hidden="true">{icono}</div>
      <h3>{titulo}</h3>
      <p>{texto}</p>
      {accion}
    </div>
  );
}
