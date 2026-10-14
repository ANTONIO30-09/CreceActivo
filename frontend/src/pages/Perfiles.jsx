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

        {/* ===== Detalle (diseño distinto al form) ===== */}
        {detalle && (
          <div className="modal-bg" onClick={() => setDetalle(null)}>
            <div className="perfil-detalle" onClick={(e) => e.stopPropagation()}>
              <header className="perfil-detalle-head">
                <div className="perfil-detalle-avatar">
                  <img src={avatarDe(detalle)} alt="" />
                </div>
                <div className="perfil-detalle-title">
                  <span className="eyebrow">PERFIL INFANTIL</span>
                  <h2>{detalle.nombre}</h2>
                  <p>{detalle.edad} años · {SEXO_LABEL[detalle.sexo] || detalle.sexo}</p>
                </div>
              </header>

              <div className="perfil-detalle-stats">
                <div className="stat-card">
                  <span className="stat-label">Peso</span>
                  <span className="stat-value">{detalle.peso_kg}<small> kg</small></span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">Estatura</span>
                  <span className="stat-value">{detalle.estatura_cm}<small> cm</small></span>
                </div>
                <div className="stat-card">
                  <span className="stat-label">Actividad</span>
                  <span className="stat-value stat-value-sm">{NIVEL_LABEL[detalle.nivel_actividad_fisica] || '—'}</span>
                </div>
              </div>

              <div className="perfil-detalle-body">
                {detalle.habitos_alimenticios && (
                  <section>
                    <h4>Hábitos alimenticios</h4>
                    <p>{detalle.habitos_alimenticios}</p>
                  </section>
                )}
                {detalle.alergias?.length > 0 && (
                  <section>
                    <h4>Alergias</h4>
                    <div className="chips-inline">
                      {detalle.alergias.map((a, i) => <span key={i} className="tag">{a}</span>)}
                    </div>
                  </section>
                )}
                {detalle.objetivos && (
                  <section>
                    <h4>Objetivos</h4>
                    <p>{detalle.objetivos}</p>
                  </section>
                )}
              </div>

              <div className="perfil-detalle-actions">
                <button className="btn-ghost" onClick={() => setDetalle(null)}>Cerrar</button>
                <button className="btn-danger" onClick={() => desactivar(detalle)}>Desactivar</button>
                <button className="primary" onClick={() => { setEditando(detalle); setDetalle(null); }}>
                  Editar
                </button>
              </div>
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
