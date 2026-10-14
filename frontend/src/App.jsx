// Router principal de la app. Define rutas y layout.
import React from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth/AuthContext';
import { ThemeProvider } from './theme';
import Sidebar from './components/Sidebar';
import ChatbotFlotante from './components/ChatbotFlotante';
import Login from './pages/Login';
import Perfiles from './pages/Perfiles';
import Nutricion from './pages/Nutricion';
import Progreso from './pages/Progreso';
import Imc from './pages/Imc';
import Chatbot from './pages/Chatbot';
import Videos from './pages/Videos';

function Layout({ children }) {
  return (
    <div className="layout">
      <Sidebar />
      <div className="content">{children}</div>
      <ChatbotFlotante />
    </div>
  );
}

function Protegida({ children }) {
  const { tutor, cargando } = useAuth();
  if (cargando) return <div className="loading-full">Cargando...</div>;
  if (!tutor) return <Navigate to="/login" replace />;
  return <Layout>{children}</Layout>;
}

function RutaPublica({ children }) {
  const { tutor, cargando } = useAuth();
  if (cargando) return <div className="loading-full">Cargando...</div>;
  if (tutor) return <Navigate to="/perfiles" replace />;
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<RutaPublica><Login /></RutaPublica>} />
          <Route path="/perfiles" element={<Protegida><Perfiles /></Protegida>} />
          <Route path="/nutricion" element={<Protegida><Nutricion /></Protegida>} />
          <Route path="/imc" element={<Protegida><Imc /></Protegida>} />
          <Route path="/chatbot" element={<Protegida><Chatbot /></Protegida>} />
          <Route path="/videos" element={<Protegida><Videos /></Protegida>} />
          <Route path="/progreso" element={<Protegida><Progreso /></Protegida>} />
          <Route path="/" element={<Navigate to="/perfiles" replace />} />
          <Route path="*" element={<Navigate to="/perfiles" replace />} />
        </Routes>
      </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}
