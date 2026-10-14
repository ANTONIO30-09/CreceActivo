// Mis hijos: lista, crea, ve en detalle, edita y desactiva perfiles.
import React, { useEffect, useState } from 'react';
import EmptyState from '../components/EmptyState';
import { perfiles as apiPerfiles } from '../api/client';

const EDADES = Array.from({ length: 9 }, (_, i) => i + 6);

const SEXO_LABEL = {
  masculino: 'Masculino',
  femenino: 'Femenino',
  otro: 'Otro',
  prefiero_no_decir: 'Prefiere no decir',
};
const NIVEL_LABEL = {
  sedentario: 'Sedentario',
  ligero: 'Ligero',
  moderado: 'Moderado',
  activo: 'Activo',
  muy_activo: 'Muy activo',
};

function avatarDe(p) {
  return p?.sexo === 'femenino'
    ? '/ilustraciones/nina.png'
    : '/ilustraciones/nino.png';
}

export default function Perfiles() {
  const [lista, setLista] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [creando, setCreando] = useState(false);
  const [detalle, setDetalle] = useState(null);
  const [editando, setEditando] = useState(null);

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

  function datosDesdeForm(e) {
    const d = new FormData(e.target);
    return {
      nombre: d.get('nombre'),
      edad: Number(d.get('edad')),
      sexo: d.get('sexo'),
      peso_kg: Number(d.get('peso_kg')),
      estatura_cm: Number(d.get('estatura_cm')),
      nivel_actividad_fisica: d.get('nivel_actividad_fisica'),
      habitos_alimenticios: d.get('habitos_alimenticios') || null,
      alergias: (d.get('alergias') || '').split(',').map(s => s.trim()).filter(Boolean),
      objetivos: d.get('objetivos') || null,
    };
  }

  async function onSubmitForm(e) {
    e.preventDefault();
    const body = datosDesdeForm(e);
    try {
      if (editando) {
        await apiPerfiles.editar(editando.id, body);
        setEditando(null);
      } else {
        await apiPerfiles.crear(body);
        setCreando(false);
      }
      cargar();
    } catch (err) {
      alert(err.detail || err.message);
    }
  }

  async function desactivar(p) {
    if (!confirm(`¿Desactivar el perfil de ${p.nombre}? Podrás volver a crearlo luego.`)) return;
    try {
      await apiPerfiles.eliminar(p.id);
      setDetalle(null);
      cargar();
    } catch (err) {
      alert(err.detail || err.message);
    }
  }

  const formAbierto = creando || editando;

  return (
    <>
      <main>
        <div className="page-head">
          <div>
            <h1>Mis hijos</h1>
            <p>Registra y gestiona los perfiles infantiles de tu familia.</p>
          </div>
          <button className="primary" onClick={() => setCreando(true)}>
            + Agregar hijo/a
          </button>
        </div>

        {error && <div className="notice warn">Error: {error}</div>}
        {cargando && <p>Cargando...</p>}

        {!cargando && lista.length === 0 && (
          <EmptyState
            imagen="/ilustraciones/nino-nina.png"
            titulo="Aún no registraste ningún hijo"
            texto="Empieza agregando el perfil de tu pequeño/a para acompañar sus hábitos."
            accion={<button className="primary" onClick={() => setCreando(true)}>Crear el primero</button>}
          />
        )}

        {!cargando && lista.length > 0 && (
          <div className="perfiles-grid">
            {lista.map((p) => (
              <button
                key={p.id}
                type="button"
                className="perfil-card perfil-card-btn"
                onClick={() => setDetalle(p)}
              >
                <div className="perfil-avatar perfil-avatar-img">
                  <img src={avatarDe(p)} alt="" />
                </div>
                <h3>{p.nombre}</h3>
                <p className="perfil-meta">{p.edad} años · {SEXO_LABEL[p.sexo] || p.sexo}</p>
                <p className="perfil-meta">{p.peso_kg} kg · {p.estatura_cm} cm</p>
                <span className="perfil-hint">Ver detalle</span>
              </button>
            ))}
          </div>
        )}

        {/* ===== Detalle extravagante ===== */}
        {detalle && (
          <div className="modal-bg modal-bg-hero" onClick={() => setDetalle(null)}>
            <div
              className={'kid-hero kid-hero-' + (detalle.sexo === 'femenino' ? 'girl' : 'boy')}
              onClick={(e) => e.stopPropagation()}
            >
              {/* Fondo decorativo */}
              <div className="kid-bg" aria-hidden="true">
                <span className="kid-blob kid-blob-1" />
                <span className="kid-blob kid-blob-2" />
                <span className="kid-blob kid-blob-3" />
                <span className="kid-star kid-star-1">✦</span>
                <span className="kid-star kid-star-2">✦</span>
                <span className="kid-star kid-star-3">✦</span>
                <span className="kid-star kid-star-4">✦</span>
              </div>

              <button className="kid-cerrar" onClick={() => setDetalle(null)} aria-label="Cerrar">✕</button>

              {/* Hero con avatar grande */}
              <header className="kid-top">
                <div className="kid-avatar-glow">
                  <div className="kid-avatar-ring" />
                  <div className="kid-avatar-ring kid-avatar-ring-2" />
                  <img src={avatarDe(detalle)} alt="" className="kid-avatar" />
                </div>
                <div className="kid-title">
                  <span className="kid-kicker">PERFIL INFANTIL</span>
                  <h1>{detalle.nombre}</h1>
                  <div className="kid-pills">
                    <span className="kid-pill">🎂 {detalle.edad} años</span>
                    <span className="kid-pill">
                      {detalle.sexo === 'femenino' ? '♀' : detalle.sexo === 'masculino' ? '♂' : '✦'}
                      {' '}{SEXO_LABEL[detalle.sexo] || detalle.sexo}
                    </span>
                    <span className="kid-pill kid-pill-live">
                      <i /> Activo
                    </span>
                  </div>
                </div>
              </header>

              {/* Stats grandes con gráficos circulares */}
              <section className="kid-stats">
                <div className="kid-stat">
                  <div className="kid-stat-ring" style={{ '--pct': Math.min(100, (detalle.peso_kg / 60) * 100) }}>
                    <svg viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="42" className="kid-ring-bg" />
                      <circle cx="50" cy="50" r="42" className="kid-ring-fg" />
                    </svg>
                    <div className="kid-stat-val">
                      <strong>{detalle.peso_kg}</strong>
                      <span>kg</span>
                    </div>
                  </div>
                  <span className="kid-stat-lbl">Peso</span>
                </div>

                <div className="kid-stat">
                  <div className="kid-stat-ring" style={{ '--pct': Math.min(100, (detalle.estatura_cm / 180) * 100) }}>
                    <svg viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="42" className="kid-ring-bg" />
                      <circle cx="50" cy="50" r="42" className="kid-ring-fg" />
                    </svg>
                    <div className="kid-stat-val">
                      <strong>{detalle.estatura_cm}</strong>
                      <span>cm</span>
                    </div>
                  </div>
                  <span className="kid-stat-lbl">Estatura</span>
                </div>

                <div className="kid-stat">
                  <div className="kid-stat-ring kid-stat-ring-energia" style={{ '--pct': 40 + (['sedentario','ligero','moderado','activo','muy_activo'].indexOf(detalle.nivel_actividad_fisica) * 15) }}>
                    <svg viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="42" className="kid-ring-bg" />
                      <circle cx="50" cy="50" r="42" className="kid-ring-fg" />
                    </svg>
                    <div className="kid-stat-val">
                      <strong>⚡</strong>
                    </div>
                  </div>
                  <span className="kid-stat-lbl">{NIVEL_LABEL[detalle.nivel_actividad_fisica] || '—'}</span>
                </div>
              </section>

              {/* Cuerpo con tarjetas coloridas */}
              <section className="kid-body">
                {detalle.habitos_alimenticios && (
                  <div className="kid-block kid-block-green">
                    <div className="kid-block-ico">🍽</div>
                    <div className="kid-block-txt">
                      <h3>Hábitos alimenticios</h3>
                      <p>{detalle.habitos_alimenticios}</p>
                    </div>
                  </div>
                )}

                {detalle.alergias?.length > 0 && (
                  <div className="kid-block kid-block-red">
                    <div className="kid-block-ico">⚠</div>
                    <div className="kid-block-txt">
                      <h3>Alergias a tener en cuenta</h3>
                      <div className="kid-tags">
                        {detalle.alergias.map((a, i) => (
                          <span key={i} className="kid-tag">{a}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {detalle.objetivos && (
                  <div className="kid-block kid-block-amber">
                    <div className="kid-block-ico">🎯</div>
                    <div className="kid-block-txt">
                      <h3>Objetivo familiar</h3>
                      <p>{detalle.objetivos}</p>
                    </div>
                  </div>
                )}

                {!detalle.habitos_alimenticios && !detalle.alergias?.length && !detalle.objetivos && (
                  <div className="kid-block kid-block-empty">
                    <div className="kid-block-ico">✨</div>
                    <div className="kid-block-txt">
                      <h3>Sin datos adicionales</h3>
                      <p>Edita el perfil para añadir hábitos, alergias u objetivos.</p>
                    </div>
                  </div>
                )}
              </section>

              {/* Acciones grandes */}
              <footer className="kid-acciones">
                <button className="kid-btn kid-btn-ghost" onClick={() => setDetalle(null)}>
                  Cerrar
                </button>
                <button className="kid-btn kid-btn-danger" onClick={() => desactivar(detalle)}>
                  Desactivar perfil
                </button>
                <button
                  className="kid-btn kid-btn-primary"
                  onClick={() => { setEditando(detalle); setDetalle(null); }}
                >
                  ✎ Editar perfil
                </button>
              </footer>
            </div>
          </div>
        )}

        {/* ===== Form crear/editar ===== */}
        {formAbierto && (
          <div className="modal-bg" onClick={() => { setCreando(false); setEditando(null); }}>
            <form className="modal modal-lg" onSubmit={onSubmitForm} onClick={(e) => e.stopPropagation()}>
              <header className="modal-head">
                <div>
                  <span className="eyebrow">{editando ? 'EDITAR PERFIL' : 'NUEVO PERFIL'}</span>
                  <h2>{editando ? `Editar a ${editando.nombre}` : 'Agregar hijo/a'}</h2>
                  <p>Completa los datos para acompañar sus hábitos saludables.</p>
                </div>
              </header>

              <section className="modal-section">
                <h3 className="modal-section-title">Datos básicos</h3>
                <div className="modal-grid">
                  <label className="field span-2">Nombre
                    <input name="nombre" required maxLength={60} defaultValue={editando?.nombre || ''} placeholder="¿Cómo se llama?" />
                  </label>
                  <label className="field">Edad
                    <select name="edad" required defaultValue={editando?.edad ?? 8}>
                      {EDADES.map((e) => <option key={e} value={e}>{e} años</option>)}
                    </select>
                  </label>
                  <label className="field">Sexo
                    <select name="sexo" required defaultValue={editando?.sexo || 'masculino'}>
                      <option value="masculino">Masculino</option>
                      <option value="femenino">Femenino</option>
                      <option value="otro">Otro</option>
                      <option value="prefiero_no_decir">Prefiero no decir</option>
                    </select>
                  </label>
                </div>
              </section>

              <section className="modal-section">
                <h3 className="modal-section-title">Cuerpo y actividad</h3>
                <div className="modal-grid cols-3">
                  <label className="field">Peso (kg)
                    <input name="peso_kg" type="number" step="0.1" min="1" required defaultValue={editando?.peso_kg ?? ''} placeholder="Ej. 28" />
                  </label>
                  <label className="field">Estatura (cm)
                    <input name="estatura_cm" type="number" step="0.1" min="1" required defaultValue={editando?.estatura_cm ?? ''} placeholder="Ej. 132" />
                  </label>
                  <label className="field">Nivel de actividad
                    <select name="nivel_actividad_fisica" required defaultValue={editando?.nivel_actividad_fisica || 'ligero'}>
                      <option value="sedentario">Sedentario</option>
                      <option value="ligero">Ligero</option>
                      <option value="moderado">Moderado</option>
                      <option value="activo">Activo</option>
                      <option value="muy_activo">Muy activo</option>
                    </select>
                  </label>
                </div>
              </section>

              <section className="modal-section">
                <h3 className="modal-section-title">Extras (opcional)</h3>
                <div className="modal-grid">
                  <label className="field span-2">Alergias
                    <input name="alergias" defaultValue={(editando?.alergias || []).join(', ')} placeholder="Separadas por coma: lactosa, maní…" />
                  </label>
                  <label className="field span-2">Hábitos alimenticios
                    <textarea name="habitos_alimenticios" maxLength={500} rows={2} defaultValue={editando?.habitos_alimenticios || ''}
                      placeholder="Ej. Come poca verdura, le gusta la fruta, desayuna poco." />
                  </label>
                  <label className="field span-2">Objetivos
                    <textarea name="objetivos" maxLength={500} rows={3} defaultValue={editando?.objetivos || ''}
                      placeholder="Ej. Probar una fruta nueva cada semana." />
                  </label>
                </div>
              </section>

              <div className="modal-actions">
                <button type="button" onClick={() => { setCreando(false); setEditando(null); }}>Cancelar</button>
                <button type="submit" className="primary">{editando ? 'Guardar cambios' : 'Guardar perfil'}</button>
              </div>
            </form>
          </div>
        )}
      </main>
    </>
  );
}
