import React from 'react';
import { useTheme } from '../theme';

export default function ThemeToggle({ className = '' }) {
  const { tema, toggle } = useTheme();
  const esOscuro = tema === 'dark';
  return (
    <button
      type="button"
      className={'theme-toggle ' + className}
      onClick={toggle}
      aria-label={esOscuro ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
      title={esOscuro ? 'Modo claro' : 'Modo oscuro'}
    >
      <span className="theme-ico">{esOscuro ? '☀' : '☾'}</span>
      <span className="theme-label">{esOscuro ? 'Claro' : 'Oscuro'}</span>
    </button>
  );
}
