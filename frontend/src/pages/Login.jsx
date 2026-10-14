// Login con Firebase Auth real (email + password).
import React, { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

export default function Login() {
  const { tutor, login, registrar } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('demo@creceactivo.bo');
  const [password, setPassword] = useState('Demo1234!');
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  if (tutor) return <Navigate to="/perfiles" replace />;

  async function onSubmit(e, modo) {
    e.preventDefault();
    setError('');
    setCargando(true);
    try {
      if (modo === 'registro') {
        await registrar(email, password);
      } else {
        await login(email, password);
      }
      navigate('/perfiles', { replace: true });
    } catch (err) {
      const msg =
        err.code === 'auth/invalid-credential' ? 'Credenciales incorrectas.' :
        err.code === 'auth/user-not-found' ? 'Usuario no encontrado.' :
        err.code === 'auth/wrong-password' ? 'Contrasena incorrecta.' :
        err.code === 'auth/email-already-in-use' ? 'El email ya esta registrado.' :
        err.code === 'auth/weak-password' ? 'Contrasena muy debil (min 6).' :
        err.message || 'Error al iniciar sesión.';
      setError(msg);
    } finally {
      setCargando(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="brand login-brand">
          <span>✳</span> <span>CreceActivo</span>
        </div>
        <h1>Bienvenido/a</h1>
        <p className="login-sub">
          Ingresa con tu cuenta para gestionar los hábitos de tus hijos.
        </p>

        <form onSubmit={(e) => onSubmit(e, 'login')}>
          <label>
            Correo electronico
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </label>
          <label>
            Contrasena
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              minLength={6}
              required
            />
          </label>

          {error && <p className="error">{error}</p>}

          <button type="submit" className="primary login-cta" disabled={cargando}>
            {cargando ? 'Entrando...' : 'Iniciar sesión'}
          </button>
        </form>

        <button
          type="button"
          className="login-register"
          onClick={(e) => onSubmit(e, 'registro')}
          disabled={cargando}
        >
          Crear cuenta nueva
        </button>

        <p className="login-note">
          Usuario demo: <strong>demo@creceactivo.bo</strong> / <strong>Demo1234!</strong>
        </p>
      </div>
    </div>
  );
}
