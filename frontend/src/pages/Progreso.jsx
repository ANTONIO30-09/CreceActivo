// Modulo 3: progreso, rachas, insignias y metas familiares.
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import EmptyState from '../components/EmptyState';
import { perfiles as apiPerfiles, progreso as apiProgreso } from '../api/client';

const TIPOS = [
  { valor: 'agua', label: 'Vasos de agua', icono: '💧' },
  { valor: 'minutos', label: 'Minutos activos', icono: '⏱' },
  { valor: 'rutina', label: 'Rutina completada', icono: '🏃' },
];

export default function Progreso() {
  const [hijos, setHijos] = useState([]);
  const [perfilId, setPerfilId] = useState('');
  const [progreso, setProgreso] = useState(null);
  const [metas, setMetas] = useState([]);
  const [catalogo, setCatalogo] = useState([]);
  const [error, setError] = useState('');
  const [form, setForm] = useState(null);

  useEffect(() => {
    apiPerfiles.listar()
      .then((d) => {
        const lista = Array.isArray(d) ? d : [];
        setHijos(lista);
        if (lista[0]) setPerfilId(lista[0].id);
      })
      .catch((e) => setError(e.detail || e.message));

    apiProgreso.insignias().then(setCatalogo).catch(() => {});
  }, []);

  useEffect(() => {
    if (!perfilId) return;
    setError('');
    Promise.all([
      apiProgreso.obtener(perfilId),
      apiProgreso.metas(perfilId),
    ])
      .then(([p, m]) => {
        setProgreso(p);
        setMetas(Array.isArray(m) ? m : []);
      })
      .catch((e) => setError(e.detail || e.message));
  }, [perfilId]);

  async function registrar(tipo) {
    const valor = prompt(
      tipo === 'agua' ? '¿Cuántos vasos de agua?' :
      tipo === 'minutos' ? '¿Cuántos minutos activos?' :
      'Rutina completada (1 para confirmar):',
      tipo === 'rutina' ? '1' : '8'
    );
    if (!valor) return;
    try {
      await apiProgreso.registrar({
        perfil_id: perfilId,
        tipo,
        valor: Number(valor),
      });
      const p = await apiProgreso.obtener(perfilId);
      setProgreso(p);
    } catch (e) {
      alert(e.detail || e.message);
    }
  }

  async function crearMeta(e) {
    e.preventDefault();
    const datos = new FormData(e.target);
    try {
      await apiProgreso.crearMeta({
        perfil_id: perfilId,
        titulo: datos.get('titulo'),
        descripcion: datos.get('descripcion') || '',
        objetivo_semanal: Number(datos.get('objetivo_semanal')),
      });
      setForm(null);
      const m = await apiProgreso.metas(perfilId);
      setMetas(Array.isArray(m) ? m : []);
    } catch (err) {
      alert(err.detail || err.message);
    }
  }

  const ganadas = new Set(progreso?.insignias_ganadas || []);

  return (
    <>
      <Header titulo="Progreso y motivación" />
      <main>
        <div className="page-head">
          <div>
            <h1>Progreso</h1>
            <p>Rachas, insignias y metas familiares.</p>
          </div>
          {hijos.length > 0 && (
            <select value={perfilId} onChange={(e) => setPerfilId(e.target.value)}>
              {hijos.map((h) => <option key={h.id} value={h.id}>{h.nombre}</option>)}
            </select>
          )}
        </div>

        {error && <div className="notice warn">{error}</div>}

        {hijos.length === 0 && (
          <EmptyState
            icono="👶"
            titulo="Primero registra a un hijo/a"
            texto="Ve a la sección Mis hijos para crear un perfil."
          />
        )}

        {perfilId && (
          <>
            <section className="stats-grid">
              <div className="stat">
                <div className="stat-icon">🔥</div>
                <div className="stat-value">{progreso?.racha_actual ?? 0}</div>
                <div className="stat-label">Racha actual</div>
              </div>
              <div className="stat">
                <div className="stat-icon">⭐</div>
                <div className="stat-value">{progreso?.mejor_racha ?? 0}</div>
                <div className="stat-label">Mejor racha</div>
              </div>
              <div className="stat">
                <div className="stat-icon">📋</div>
                <div className="stat-value">{progreso?.total_registros ?? 0}</div>
                <div className="stat-label">Registros</div>
              </div>
              <div className="stat">
                <div className="stat-icon">🏅</div>
                <div className="stat-value">{ganadas.size}</div>
                <div className="stat-label">Insignias</div>
              </div>
            </section>

            <section className="actions">
              <h2>Registrar hoy</h2>
              <div className="action-buttons">
                {TIPOS.map((t) => (
                  <button key={t.valor} className="action-btn" onClick={() => registrar(t.valor)}>
                    <span>{t.icono}</span>
                    <span>{t.label}</span>
                  </button>
                ))}
              </div>
            </section>

            <section className="metas-section">
              <div className="page-head">
                <div>
                  <h2>Metas familiares</h2>
                  <p>Define objetivos semanales de 1 a 7 días.</p>
                </div>
                <button className="primary" onClick={() => setForm({})}>+ Nueva meta</button>
              </div>

              {metas.length === 0 && (
                <EmptyState
                  icono="🎯"
                  titulo="Sin metas activas"
                  texto="Crea una meta para empezar a acompañar el progreso."
                />
              )}

              <div className="metas-list">
                {metas.map((m) => (
                  <div key={m.id} className="meta-card">
                    <div className="meta-head">
                      <h3>{m.titulo}</h3>
                      <span>{m.porcentaje}%</span>
                    </div>
                    {m.descripcion && <p>{m.descripcion}</p>}
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${m.porcentaje}%` }} />
                    </div>
                    <p className="meta-foot">
                      {m.completado_semana} de {m.objetivo_semanal} días esta semana
                    </p>
                  </div>
                ))}
              </div>
            </section>

            <section className="insignias-section">
              <h2>Insignias</h2>
              <div className="insignias-grid">
                {catalogo.map((i) => (
                  <div
                    key={i.id}
                    className={'insignia' + (ganadas.has(i.id) ? ' ganada' : ' pendiente')}
                  >
                    <div className="insignia-icon">{ganadas.has(i.id) ? '🏅' : '🔒'}</div>
                    <p>{i.nombre}</p>
                    <small>{i.tipo}: {i.meta}</small>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}

        {form && (
          <div className="modal-bg" onClick={() => setForm(null)}>
            <form className="modal" onSubmit={crearMeta} onClick={(e) => e.stopPropagation()}>
              <h2>Nueva meta</h2>
              <label>Título
                <input name="titulo" required maxLength={120} />
              </label>
              <label>Descripción
                <textarea name="descripcion" maxLength={500} rows={2} />
              </label>
              <label>Objetivo semanal (días)
                <input name="objetivo_semanal" type="number" min="1" max="7" defaultValue="3" required />
              </label>
              <div className="modal-actions">
                <button type="button" onClick={() => setForm(null)}>Cancelar</button>
                <button type="submit" className="primary">Crear</button>
              </div>
            </form>
          </div>
        )}
      </main>
    </>
  );
}
