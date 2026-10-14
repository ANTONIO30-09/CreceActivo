// Manejo de tema (light / dark) con persistencia en localStorage.
import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeCtx = createContext({ tema: 'light', toggle: () => {} });

export function ThemeProvider({ children }) {
  const [tema, setTema] = useState(() => localStorage.getItem('crece-tema') || 'light');
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', tema);
    localStorage.setItem('crece-tema', tema);
  }, [tema]);
  return (
    <ThemeCtx.Provider value={{ tema, toggle: () => setTema((t) => (t === 'light' ? 'dark' : 'light')) }}>
      {children}
    </ThemeCtx.Provider>
  );
}

export const useTheme = () => useContext(ThemeCtx);
