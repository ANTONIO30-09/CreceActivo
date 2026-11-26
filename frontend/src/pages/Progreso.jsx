import React, { useEffect, useState } from 'react';
import EmptyState from '../components/EmptyState';
import { perfiles as apiPerfiles, progreso as apiProgreso } from '../api/client';

const TIPOS = [
  { valor: 'agua',    label: 'Vasos de agua',     icono: '💧', unidad: 'vasos',   default: 8,  max: 30,  color: '#38bdf8' },
  { valor: 'minutos', label: 'Minutos activos',   icono: '⏱',  unidad: 'minutos', default: 30, max: 300, color: '#10b981' },
  { valor: 'rutina',  label: 'Rutina completada', icono: '🏃', unidad: 'rutinas', default: 1,  max: 5,   color: '#f59e0b' },
];

function avatarDe(p) {
  return p?.sexo === 'femenino' ? '/ilustraciones/nina.png' : '/ilustraciones/nino.png';
}

export default function Progreso() {
  const [hijos, setHijos] = useState([]);
  const [perfilId, setPerfilId] = useState('');
  const [progreso, setProgreso] = useState(null);
  const [metas, setMetas] = useState([]);
  const [catalogo, setCatalogo] = useState([]);
  const [error, setError] = useState('');
  const [registros, setRegistros] = useState([]);
  const [modalRegistro, setModalRegistro] = useState(null);
  const [valorRegistro, setValorRegistro] = useState('');
  const [guardando, setGuardando] = useState(false);
  const [modalMeta, setModalMeta] = useState(false);
  const [marcando, setMarcando] = useState(null);

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
      apiProgreso.registros(perfilId).catch(() => []),
    ])
      .then(([p, m, r]) => {
        setProgreso(p);
        setMetas(Array.isArray(m) ? m : []);
        setRegistros(Array.isArray(r) ? r : []);
      })
      .catch((e) => setError(e.detail || e.message));
  }, [perfilId]);

  function abrirRegistro(tipo) {
    const t = TIPOS.find((x) => x.valor === tipo);
    setValorRegistro(String(t.default));
    setModalRegistro(t);
  }

  async function confirmarRegistro(e) {
    e.preventDefault();
    const n = Number(valorRegistro);
    if (!n || n < 1) return;
    setGuardando(true);
    try {
      await apiProgreso.registrar({ perfil_id: perfilId, tipo: modalRegistro.valor, valor: n });
      const [p, r] = await Promise.all([
        apiProgreso.obtener(perfilId),
        apiProgreso.registros(perfilId).catch(() => []),
      ]);
      setProgreso(p);
      setRegistros(Array.isArray(r) ? r : []);
      setModalRegistro(null);
    } catch (err) {
      alert(err.detail || err.message);
    } finally { setGuardando(false); }
  }

  async function marcarMeta(metaId) {
    setMarcando(metaId);
    try {
      await apiProgreso.marcarMeta(metaId, new Date().toISOString().slice(0, 10));
      const [p, r] = await Promise.all([
        apiProgreso.obtener(perfilId),
        apiProgreso.registros(perfilId).catch(() => []),
      ]);
      setProgreso(p);
      setRegistros(Array.isArray(r) ? r : []);
      const m = await apiProgreso.metas(perfilId);
      setMetas(Array.isArray(m) ? m : []);
    } catch (err) {
      alert(err.detail || err.message);
    } finally { setMarcando(null); }
  }

  async function archivarMeta(metaId, titulo) {
    if (!confirm(`¿Archivar la meta "${titulo}"?`)) return;
    try {
      await apiProgreso.archivarMeta(metaId);
      const m = await apiProgreso.metas(perfilId);
      setMetas(Array.isArray(m) ? m : []);
    } catch (err) {
      alert(err.detail || err.message);
    }
  }

  async function crearMeta(e) {
    e.preventDefault();
    const d = new FormData(e.target);
    try {
      await apiProgreso.crearMeta({
        perfil_id: perfilId,
        titulo: d.get('titulo'),
        descripcion: d.get('descripcion') || '',
        objetivo_semanal: Number(d.get('objetivo_semanal')),
      });
      setModalMeta(false);
      const m = await apiProgreso.metas(perfilId);
      setMetas(Array.isArray(m) ? m : []);
    } catch (err) { alert(err.detail || err.message); }
  }

  const ganadas = new Set(progreso?.insignias_ganadas || []);
  const perfilSel = hijos.find((h) => h.id === perfilId);
  const hoy = new Date().toISOString().slice(0, 10);
  const registrosHoy = registros.filter((r) => (r.fecha || '').slice(0, 10) === hoy);

  return (
    <>
      <main>
        <div className="page-head">
          <div>
            <h1>Progreso</h1>
            <p>Rachas, insignias y metas familiares.</p>
          </div>
          {hijos.length > 0 && (
            <div className="perfil-tabs">
              {hijos.map((h) => (
                <button
                  key={h.id}
                  type="button"
                  className={'perfil-tab' + (h.id === perfilId ? ' activo' : '')}
                  onClick={() => setPerfilId(h.id)}
                >
                  <img src={avatarDe(h)} alt="" />
                  <span>{h.nombre}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {error && <div className="notice warn">{error}</div>}

        {hijos.length === 0 && (
          <EmptyState
            imagen="/ilustraciones/nino-nina.png"
            titulo="Primero registra a un hijo/a"
            texto="Ve a la sección Mis hijos para crear un perfil."
          />
        )}

        {perfilId && (
          <>
            {/* Hero con avatar y racha */}
            <section className="progreso-hero">
              {perfilSel && (
                <div className="progreso-hero-avatar">
                  <img src={avatarDe(perfilSel)} alt="" />
                </div>
              )}
              <div className="progreso-hero-info">
                <span className="eyebrow">PROGRESO DE</span>
                <h2>{perfilSel?.nombre}</h2>
                <p>{perfilSel?.edad} años · {perfilSel?.peso_kg} kg · {perfilSel?.estatura_cm} cm</p>
              </div>
              <div className="progreso-hero-racha">
                <span className="racha-fuego">🔥</span>
                <div>
                  <span className="racha-num">{progreso?.racha_actual ?? 0}</span>
                  <span className="racha-lbl">día{progreso?.racha_actual === 1 ? '' : 's'} seguidos</span>
                </div>
              </div>
            </section>

            {/* Tarjetas de stats */}
            <section className="stats-grid">
              <div className="stat-card">
                <span className="stat-icon">🔥</span>
                <span className="stat-label">Racha actual</span>
                <span className="stat-value">{progreso?.racha_actual ?? 0}</span>
                <span className="stat-hint">días seguidos</span>
              </div>
              <div className="stat-card">
                <span className="stat-icon">⭐</span>
                <span className="stat-label">Mejor racha</span>
                <span className="stat-value">{progreso?.mejor_racha ?? 0}</span>
                <span className="stat-hint">tu récord</span>
              </div>
              <div className="stat-card">
                <span className="stat-icon">📋</span>
                <span className="stat-label">Registros</span>
                <span className="stat-value">{progreso?.total_registros ?? 0}</span>
                <span className="stat-hint">en total</span>
              </div>
              <div className="stat-card">
                <span className="stat-icon">🏅</span>
                <span className="stat-label">Insignias</span>
                <span className="stat-value">{ganadas.size}</span>
                <span className="stat-hint">de {catalogo.length}</span>
              </div>
            </section>

            {/* Registrar hoy */}
            <section className="acciones-hoy">
              <header className="acciones-hoy-head">
                <h2>Registrar hoy</h2>
                <p>Suma agua, minutos o rutinas completadas.</p>
              </header>
              <div className="action-buttons">
                {TIPOS.map((t) => (
                  <button key={t.valor} className="action-btn" onClick={() => abrirRegistro(t.valor)}
                    style={{ '--accent': t.color }}>
                    <span className="action-ico">{t.icono}</span>
                    <span className="action-label">{t.label}</span>
                    <span className="action-plus">+</span>
                  </button>
                ))}
              </div>
            </section>

            {/* Registros recientes */}
            <section className="registros-section">
              <header className="registros-head">
                <h2>Registros recientes</h2>
                <span className="registros-count">{registrosHoy.length} de hoy</span>
              </header>
              {registros.length === 0 ? (
                <div className="registros-vacio">
                  Aún no hay registros. Usa los botones de arriba para empezar.
                </div>
              ) : (
                <div className="registros-list">
                  {registros.slice(-8).reverse().map((r) => {
                    const t = TIPOS.find((x) => x.valor === r.tipo) || {};
                    const esHoy = (r.fecha || '').slice(0, 10) === hoy;
                    return (
                      <div key={r.id} className={'registro-item' + (esHoy ? ' hoy' : '')}>
                        <span className="registro-ico" style={{ background: (t.color || '#10b981') + '22', borderColor: (t.color || '#10b981') + '66' }}>
                          {t.icono || '•'}
                        </span>
                        <div className="registro-info">
                          <strong>{t.label || r.tipo}</strong>
                          <span>{r.fecha}{esHoy ? ' · hoy' : ''}</span>
                        </div>
                        <span className="registro-valor" style={{ color: t.color || '#a7f3d0' }}>
                          {r.valor}<small> {t.unidad || ''}</small>
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}
            </section>

            {/* Metas */}
            <section className="metas-section">
              <div className="section-heading">
                <div>
                  <h2>Metas familiares</h2>
                  <p>Objetivos semanales de 1 a 7 días.</p>
                </div>
                <button className="primary" onClick={() => setModalMeta(true)}>+ Nueva meta</button>
              </div>

              {metas.length === 0 ? (
                <EmptyState icono="🎯" titulo="Sin metas activas" texto="Crea una meta para acompañar el progreso." />
              ) : (
                <div className="metas-list">
                  {metas.map((m) => {
                    const completo = m.completado_semana >= m.objetivo_semanal;
                    return (
                      <div key={m.id} className={'meta-card' + (completo ? ' completa' : '')}>
                        <div className="meta-head">
                          <div>
                            <h3>{m.titulo}</h3>
                            {m.descripcion && <p className="meta-desc">{m.descripcion}</p>}
                          </div>
                          <span className="meta-pct">{m.porcentaje}%</span>
                        </div>

                        <div className="progress-bar">
                          <div className="progress-fill" style={{ width: `${m.porcentaje}%` }} />
                        </div>

                        <div className="meta-foot-row">
                          <span className="meta-foot">
                            {m.completado_semana} de {m.objetivo_semanal} días esta semana
                          </span>
                          <div className="meta-acciones">
                            <button
                              className="meta-archivar"
                              onClick={() => archivarMeta(m.id, m.titulo)}
                              title="Archivar meta"
                            >✕</button>
                            <button
                              className={'meta-marcar' + (completo ? ' ya' : '')}
                              onClick={() => marcarMeta(m.id)}
                              disabled={marcando === m.id || completo}
                            >
                              {marcando === m.id ? 'Marcando…' : completo ? '✓ Completa' : '✓ Marcar hoy'}
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </section>

            {/* Insignias */}
            <section className="insignias-section">
              <h2>Insignias</h2>
              <div className="insignias-grid">
                {catalogo.map((i) => (
                  <div key={i.id} className={'insignia' + (ganadas.has(i.id) ? ' ganada' : ' pendiente')}>
                    <div className="insignia-icon">{ganadas.has(i.id) ? '🏅' : '🔒'}</div>
                    <p>{i.nombre}</p>
                    <small>{i.tipo}: {i.meta}</small>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}

        {/* Modal registro */}
        {modalRegistro && (
          <div className="modal-bg" onClick={() => setModalRegistro(null)}>
            <form className="modal modal-sm" onSubmit={confirmarRegistro} onClick={(e) => e.stopPropagation()}>
              <header className="modal-head">
                <div>
                  <span className="eyebrow">REGISTRAR</span>
                  <h2>{modalRegistro.icono} {modalRegistro.label}</h2>
                  <p>¿Cuántos {modalRegistro.unidad} hoy?</p>
                </div>
              </header>
              <section className="modal-section" style={{ paddingTop: 8 }}>
                <div className="num-step">
                  <button type="button" onClick={() => setValorRegistro(String(Math.max(1, Number(valorRegistro) - 1)))}>−</button>
                  <input
                    type="number" min="1" max={modalRegistro.max}
                    value={valorRegistro}
                    onChange={(e) => setValorRegistro(e.target.value)}
                    autoFocus
                  />
                  <button type="button" onClick={() => setValorRegistro(String(Math.min(modalRegistro.max, Number(valorRegistro) + 1)))}>+</button>
                </div>
                <div className="num-quick">
                  {[1, 5, 10, 15, 30].filter((n) => n <= modalRegistro.max).map((n) => (
                    <button key={n} type="button" onClick={() => setValorRegistro(String(n))}>{n}</button>
                  ))}
                </div>
              </section>
              <div className="modal-actions">
                <button type="button" onClick={() => setModalRegistro(null)}>Cancelar</button>
                <button type="submit" className="primary" disabled={guardando}>
                  {guardando ? 'Guardando…' : 'Registrar'}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Modal nueva meta */}
        {modalMeta && (
          <div className="modal-bg" onClick={() => setModalMeta(false)}>
            <form className="modal modal-lg" onSubmit={crearMeta} onClick={(e) => e.stopPropagation()}>
              <header className="modal-head">
                <div>
                  <span className="eyebrow">NUEVA META</span>
                  <h2>Meta familiar</h2>
                  <p>Objetivo semanal de 1 a 7 días.</p>
                </div>
              </header>
              <section className="modal-section">
                <div className="modal-grid">
                  <label className="field span-2">Título
                    <input name="titulo" required maxLength={120} placeholder="Ej. Caminar juntos" />
                  </label>
                  <label className="field span-2">Descripción
                    <textarea name="descripcion" maxLength={500} rows={2} placeholder="¿Cómo lo haremos?" />
                  </label>
                  <label className="field">Días por semana
                    <input name="objetivo_semanal" type="number" min="1" max="7" defaultValue="3" required />
                  </label>
                </div>
              </section>
              <div className="modal-actions">
                <button type="button" onClick={() => setModalMeta(false)}>Cancelar</button>
                <button type="submit" className="primary">Crear meta</button>
              </div>
            </form>
          </div>
        )}
      </main>
    </>
  );
}
