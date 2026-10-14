// Contexto de autenticacion con Firebase real.
import React, { createContext, useContext, useEffect, useState } from 'react';
import {
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
  createUserWithEmailAndPassword,
  updateProfile,
} from 'firebase/auth';
import { auth } from './firebase';
import { tutores } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [tutor, setTutor] = useState(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (user) => {
      setTutor(user
        ? { uid: user.uid, email: user.email, nombre: user.displayName || '', demo: false }
        : null);
      setCargando(false);
    });
    return () => unsub();
  }, []);

  async function login(email, password) {
    const cred = await signInWithEmailAndPassword(auth, email, password);
    const nombre = cred.user.displayName || '';
    try { await tutores.sync({ nombre }); } catch { /* no bloquea */ }
    return { uid: cred.user.uid, email: cred.user.email, nombre, demo: false };
  }

  async function registrar(email, password, nombre = '') {
    const cred = await createUserWithEmailAndPassword(auth, email, password);
    if (nombre) {
      try {
        await updateProfile(cred.user, { displayName: nombre });
      } catch {
        // si falla el displayName, seguimos (no bloquea el registro)
      }
    }
    try { await tutores.sync({ nombre }); } catch { /* no bloquea */ }
    return { uid: cred.user.uid, email: cred.user.email, nombre, demo: false };
  }

  async function logout() {
    await signOut(auth);
  }

  return (
    <AuthContext.Provider value={{ tutor, cargando, login, registrar, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider');
  return ctx;
}
