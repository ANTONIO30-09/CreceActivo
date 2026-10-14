// Login / Registro con Firebase Auth.
import React, { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import BallsPhysics from '../components/BallsPhysics';
import ThemeToggle from '../components/ThemeToggle';

const DOMINIO = '@creceactivo.bo';

export default function Login() {
  const { tutor, login, registrar } = useAuth();
  const navigate = useNavigate();
  const [modo, setModo] = useState('login'); // 'login' | 'registro'
  const [nombre, setNombre] = useState('');
  const [usuario, setUsuario] = useState(''); // parte antes del @
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  if (tutor) return <Navigate to="/perfiles" replace />;

  function limpiar() {
    setError('');
    setPassword('');
    setPassword2('');
  }

  function cambiarModo(m) {
    setModo(m);
    limpiar();
  }

  async function onSubmit(e) {
    e.preventDefault();
    setError('');

    const email = (usuario.trim().includes('@') ? usuario.trim() : usuario.trim() + DOMINIO).toLowerCase();

    if (!email || !email.includes('@')) {
      setError('Ingresa un correo válido.');
      return;
    }
    if (password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres.');
      return;
    }
    if (modo === 'registro') {
      if (!nombre.trim()) {
        setError('Ingresa tu nombre.');
        return;
      }
      if (password !== password2) {
        setError('Las contraseñas no coinciden.');
        return;
      }
    }

    setCargando(true);
    try {
      if (modo === 'registro') {
        await registrar(email, password, nombre.trim());
      } else {
        await login(email, password);
      }
      navigate('/perfiles', { replace: true });
    } catch (err) {
      const msg =
        err.code === 'auth/invalid-credential'    ? 'Credenciales incorrectas.' :
        err.code === 'auth/user-not-found'        ? 'Usuario no encontrado.' :
        err.code === 'auth/wrong-password'        ? 'Contraseña incorrecta.' :
        err.code === 'auth/email-already-in-use'  ? 'Ese correo ya está registrado. Inicia sesión o usa otro.' :
        err.code === 'auth/weak-password'         ? 'Contraseña muy débil (mínimo 6 caracteres).' :
        err.code === 'auth/invalid-email'         ? 'Correo inválido.' :
        err.code === 'auth/operation-not-allowed' ? 'El registro con correo/contraseña está deshabilitado en Firebase.' :
        err.message || 'Error inesperado.';
      setError(msg);
    } finally {
      setCargando(false);
    }
  }

  return (
    <div className="login-page">
      <ThemeToggle className="theme-toggle-login" />
      <BallsPhysics />

      <div className="login-card">
        <div className="brand login-brand">
          <div className="brand-logo-wrap">
            <img src="/logo.png" alt="" className="brand-logo" />
          </div>
          <span>CreceActivo</span>
        </div>

        <div className="login-tabs" role="tablist">
          <button
            type="button"
            className={'login-tab' + (modo === 'login' ? ' activo' : '')}
            onClick={() => cambiarModo('login')}
            role="tab"
            aria-selected={modo === 'login'}
          >
            Iniciar sesión
          </button>
          <button
            type="button"
            className={'login-tab' + (modo === 'registro' ? ' activo' : '')}
            onClick={() => cambiarModo('registro')}
            role="tab"
            aria-selected={modo === 'registro'}
          >
            Crear cuenta
          </button>
        </div>

        <h1>{modo === 'registro' ? 'Crea tu cuenta' : 'Bienvenido/a'}</h1>
        <p className="login-sub">
          {modo === 'registro'
            ? 'Regístrate para acompañar los hábitos de tu familia.'
            : 'Ingresa con tu cuenta para gestionar los hábitos de tus hijos.'}
        </p>

        <form onSubmit={onSubmit} autoComplete="on">
          {modo === 'registro' && (
            <label>
              Nombre
              <input
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                placeholder="Ej. María López"
                autoComplete="name"
                maxLength={80}
                required
              />
            </label>
          )}

          <label>
            {modo === 'registro' ? 'Correo institucional' : 'Correo electrónico'}
            <div className="email-input">
              <input
                type="text"
                value={usuario}
                onChange={(e) => setUsuario(e.target.value.replace(/\s/g, ''))}
                placeholder="tu.nombre"
                autoComplete="username"
                spellCheck={false}
                required
              />
              {!usuario.includes('@') && <span className="email-suffix">{DOMINIO}</span>}
            </div>
          </label>

          <label>
            Contraseña
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete={modo === 'registro' ? 'new-password' : 'current-password'}
              minLength={6}
              placeholder="Mínimo 6 caracteres"
              required
            />
          </label>

          {modo === 'registro' && (
            <label>
              Confirmar contraseña
              <input
                type="password"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                autoComplete="new-password"
                minLength={6}
                placeholder="Repite la contraseña"
                required
              />
            </label>
          )}

          {error && <p className="error">{error}</p>}

          <button type="submit" className="primary login-cta" disabled={cargando}>
            {cargando
              ? (modo === 'registro' ? 'Creando cuenta…' : 'Entrando…')
              : (modo === 'registro' ? 'Crear mi cuenta' : 'Iniciar sesión')}
          </button>
        </form>

        <p className="login-nota">
          {modo === 'login'
            ? '¿No tienes cuenta? Toca "Crear cuenta" arriba.'
            : 'Al crear la cuenta aceptas usar la plataforma de forma responsable con tu familia.'}
        </p>
      </div>
    </div>
  );
}
