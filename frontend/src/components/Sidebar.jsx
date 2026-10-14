import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import ThemeToggle from './ThemeToggle';

const Icon = ({ name }) => {
  const paths = {
    hijos: <><circle cx="12" cy="8" r="3.2"/><path d="M4 20c0-3.6 3.6-6 8-6s8 2.4 8 6"/></>,
    nutricion: <><path d="M5 3v10a4 4 0 0 0 4 4h1v4"/><path d="M8 3v8"/><path d="M16 3c-1.5 2-2.5 4-2.5 6.5 0 1.5.5 2.5 1.5 3h3.5"/></>,
    imc: <><path d="M4 4h16v16H4z"/><path d="M12 8v8"/><path d="M8 12h8"/></>,
    chatbot: <><path d="M21 12a8 8 0 1 1-3.1-6.3"/><path d="M8 12h.01M12 12h.01M16 12h.01"/></>,
    videos: <><rect x="3" y="6" width="13" height="12" rx="2"/><path d="m22 8-6 4 6 4z"/></>,
    progreso: <><path d="M3 20h18"/><path d="M7 20V10"/><path d="M12 20V4"/><path d="M17 20v-7"/></>,
  };
  return (
    <svg className="nav-ico" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  );
};

const NAV_ITEMS = [
  { to: '/perfiles',   ico: 'hijos',    label: 'Mis hijos' },
  { to: '/nutricion',  ico: 'nutricion', label: 'Nutrición' },
  { to: '/imc',        ico: 'imc',       label: 'IMC orientativo' },
  { to: '/chatbot',    ico: 'chatbot',   label: 'Chatbot' },
  { to: '/videos',     ico: 'videos',    label: 'Videos' },
  { to: '/progreso',   ico: 'progreso',  label: 'Progreso' },
];

export default function Sidebar() {
  const { tutor, logout } = useAuth();
  const [colapsado, setColapsado] = useState(false);

  return (
    <aside className={'sidebar' + (colapsado ? ' colapsado' : '')}>
      <header className="side-head">
        <a className="brand" href="/" aria-label="CreceActivo, inicio">
          <img src="/logo.png" alt="" className="brand-logo" />
          {!colapsado && <span>CreceActivo</span>}
        </a>
        <ThemeToggle className="theme-toggle-side" />
        <button
          className="side-toggle"
          onClick={() => setColapsado((c) => !c)}
          aria-label={colapsado ? 'Expandir menú' : 'Colapsar menú'}
          title={colapsado ? 'Expandir' : 'Colapsar'}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
            strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            {colapsado
              ? <path d="m9 6 6 6-6 6" />
              : <path d="m15 6-6 6 6 6" />}
          </svg>
        </button>
      </header>

      {!colapsado && (
        <div className="side-lema">
          <span>Un paso a la vez</span>
          <p>Acompañamos el aprendizaje de hábitos en familia.</p>
        </div>
      )}

      <nav aria-label="Navegación principal">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => 'nav-item' + (isActive ? ' active' : '')}
            title={colapsado ? item.label : undefined}
          >
            <Icon name={item.ico} />
            {!colapsado && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      {tutor && (
        <div className="side-user">
          {!colapsado && <p className="side-user-email" title={tutor.email}>{tutor.email}</p>}
          <button onClick={logout} className="side-logout" title={colapsado ? 'Cerrar sesión' : undefined}>
            {colapsado ? (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" style={{ width: 18, height: 18 }}>
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>
              </svg>
            ) : 'Cerrar sesión'}
          </button>
        </div>
      )}
    </aside>
  );
}
