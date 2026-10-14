// Sidebar de navegacion principal. Reutiliza estilos del sidebar actual.
import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

const NAV_ITEMS = [
  { to: '/perfiles', icono: '👧', label: 'Mis hijos' },
  { to: '/nutricion', icono: '🥗', label: 'Nutricion' },
  { to: '/imc', icono: '📏', label: 'IMC orientativo' },
  { to: '/chatbot', icono: '💬', label: 'Chatbot' },
  { to: '/videos', icono: '🎬', label: 'Videos' },
  { to: '/progreso', icono: '🏃', label: 'Progreso' },
];

export default function Sidebar() {
  const { tutor, logout } = useAuth();

  return (
    <aside className="sidebar">
      <a className="brand" href="/" aria-label="CreceActivo, inicio">
        <img src="/logo.png" alt="" className="brand-logo" />
        <span>CreceActivo</span>
      </a>

      <p className="side-label">ESPACIO PARA FAMILIAS</p>

      <nav aria-label="Navegacion principal">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              isActive ? 'nav-item active' : 'nav-item'
            }
          >
            <span aria-hidden="true">{item.icono}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="side-note">
        <span>Un paso a la vez.</span>
        <p>Acompañamos el aprendizaje de hábitos en familia.</p>
      </div>

      {tutor && (
        <div className="side-user">
          <p className="side-user-email" title={tutor.email}>
            {tutor.email}
          </p>
          <button onClick={logout} className="side-logout">
            Cerrar sesión
          </button>
        </div>
      )}
    </aside>
  );
}
