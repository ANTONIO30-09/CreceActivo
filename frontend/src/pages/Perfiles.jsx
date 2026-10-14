// Mis hijos: lista, crea y selecciona perfiles infantiles.
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import EmptyState from '../components/EmptyState';
import { perfiles as apiPerfiles } from '../api/client';
import { useAuth } from '../auth/AuthContext';

const EDADES = Array.from({ length: 9 }, (_, i) => i + 6);

export default function Perfiles() {
  const { tutor } = useAuth();
  const [lista, setLista] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [form, setForm] = useState(null);

  async function cargar() {
    setCargando(true);
    setError('');
    try {
      const data = await apiPerfiles.listar();
      setLista(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e.detail || e.message);
      setLista([]);
    } finally {
      setCargando(false);
    }
  }

  useEffect(() => { cargar(); }, []);

  async function crear(e) {
    e.preventDefault();
    const datos = new FormData(e.target);
    const body = {
      nombre: datos.get('nombre'),
      edad: Number(datos.get('edad')),
      sexo: datos.get('sexo'),
      peso_kg: Number(datos.get('peso_kg')),
      estatura_cm: Number(datos.get('estatura_cm')),
      nivel_actividad_fisica: datos.get('nivel_actividad_fisica'),
      habitos_alimenticios: datos.get('habitos_alimenticios') || null,
      alergias: (datos.get('alergias') || '').split(',').map(s => s.trim()).filter(Boolean),
      objetivos: datos.get('objetivos') || null,
    };
    try {
      await apiPerfiles.crear(body);
      setForm(null);
      cargar();
    } catch (err) {
      alert(err.detail || err.message);
    }
  }

  return (
    <>
      <Header titulo="Mis hijos" />
      <main>
        <div className="page-head">
          <div>
            <h1>Mis hijos</h1>
            <p>Registra y gestiona los perfiles infantiles de tu familia.</p>
          </div>
          <button className="primary" onClick={() => setForm({})}>
            + Agregar hijo/a
          </button>
        </div>

        {error && <div className="notice warn">Error: {error}</div>}

        {cargando && <p>Cargando...</p>}

        {!cargando && lista.length === 0 && (
          <EmptyState
            icono="👶"
            titulo="Aún no registraste ningún hijo"
            texto="Empieza agregando el perfil de tu pequeño/a para acompañar sus hábitos."
            accion={<button className="primary" onClick={() => setForm({})}>Crear el primero</button>}
          />
        )}

        {!cargando && lista.length > 0 && (
          <div className="perfiles-grid">
            {lista.map((p) => (
              <div key={p.id} className="perfil-card">
                <div className="perfil-avatar">{p.nombre?.[0] || '?'}</div>
                <h3>{p.nombre}</h3>
                <p className="perfil-meta">{p.edad} años · {p.sexo}</p>
                <p className="perfil-meta">{p.peso_kg} kg · {p.estatura_cm} cm</p>
              </div>
            ))}
          </div>
        )}

        {form && (
          <div className="modal-bg" onClick={() => setForm(null)}>
            <form className="modal" onSubmit={crear} onClick={(e) => e.stopPropagation()}>
              <h2>Nuevo hijo/a</h2>
              <label>Nombre
                <input name="nombre" required maxLength={60} />
              </label>
              <label>Edad
                <select name="edad" required defaultValue="8">
                  {EDADES.map((e) => <option key={e} value={e}>{e} años</option>)}
                </select>
              </label>
              <label>Sexo
                <select name="sexo" required defaultValue="masculino">
                  <option value="masculino">Masculino</option>
                  <option value="femenino">Femenino</option>
                  <option value="otro">Otro</option>
                  <option value="prefiero_no_decir">Prefiero no decir</option>
                </select>
              </label>
              <label>Peso (kg)
                <input name="peso_kg" type="number" step="0.1" min="1" required />
              </label>
              <label>Estatura (cm)
                <input name="estatura_cm" type="number" step="0.1" min="1" required />
              </label>
              <label>Nivel de actividad
                <select name="nivel_actividad_fisica" required defaultValue="ligero">
                  <option value="sedentario">Sedentario</option>
                  <option value="ligero">Ligero</option>
                  <option value="moderado">Moderado</option>
                  <option value="activo">Activo</option>
                  <option value="muy_activo">Muy activo</option>
                </select>
              </label>
              <label>Alergias (separadas por coma)
                <input name="alergias" placeholder="Ninguna si lo dejas vacio" />
              </label>
              <label>Objetivos
                <textarea name="objetivos" maxLength={500} rows={2} />
              </label>
              <div className="modal-actions">
                <button type="button" onClick={() => setForm(null)}>Cancelar</button>
                <button type="submit" className="primary">Guardar</button>
              </div>
            </form>
          </div>
        )}
      </main>
    </>
  );
}
