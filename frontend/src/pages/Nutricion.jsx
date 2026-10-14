// Modulo 2: guias y menus conectados al backend real.
import React, { useEffect, useMemo, useState } from 'react';
import EmptyState from '../components/EmptyState';
import { nutricion } from '../api/client';

const RANGOS = ['Todas las edades', '6-8 años', '9-11 años', '12-14 años'];
const ICONOS = { Habitos: '✦', Meriendas: '◒', Alimentacion: '◇' };
const COLORES = ['sage', 'peach', 'lavender', 'sand'];

export default function Nutricion() {
  const [guias, setGuias] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [edad, setEdad] = useState(RANGOS[0]);
  const [detalle, setDetalle] = useState(null);

  useEffect(() => {
    setCargando(true);
    setError('');
    nutricion.guias()
      .then((data) => setGuias(Array.isArray(data) ? data : []))
      .catch((e) => setError(e.detail || e.message))
      .finally(() => setCargando(false));
  }, []);

  const visibles = useMemo(() => {
    const q = query.trim().toLowerCase();
    return guias.filter((g) => {
      const okQ = !q || g.titulo.toLowerCase().includes(q);
      const okE = edad === RANGOS[0] || g.rango_edad === edad;
      return okQ && okE;
    });
  }, [guias, query, edad]);

  return (
    <>
      <main>
        <div className="page-head">
          <div>
            <h1>Nutrición</h1>
            <p>Guías y menús validados por profesionales de la nutrición.</p>
          </div>
          <span className="pill-count">{visibles.length} guías</span>
        </div>

        {error && (
          <div className="notice warn">
            No se pudo conectar con el backend. Verifica que esté corriendo en{' '}
            <code>localhost:8000</code>.
          </div>
        )}

        <section className="hero small">
          <div>
            <span className="eyebrow">CRECER JUNTOS</span>
            <h1>Pequeños hábitos.{'\n'}Grandes comienzos.</h1>
            <p>Contenido aprobado por nutricionistas, listo para tu familia.</p>
          </div>
        </section>

        <div className="filters-row">
          <label className="field grow">Buscar guía
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Escribe un título…"
            />
          </label>
          <label className="field w-220">Rango de edad
            <select value={edad} onChange={(e) => setEdad(e.target.value)}>
              {RANGOS.map((r) => <option key={r}>{r}</option>)}
            </select>
          </label>
        </div>

        {cargando && <p>Cargando guías…</p>}

        {!cargando && visibles.length === 0 && (
          <EmptyState
            icono="🥗"
            titulo="No hay guías disponibles"
            texto={error ? 'Revisa la conexión con el backend.' : 'Prueba con otro filtro.'}
          />
        )}

        {!cargando && visibles.length > 0 && (
          <div className="cards">
            {visibles.map((g, i) => (
              <article key={g.id} className="card card-clickable" onClick={() => setDetalle(g)}>
                <div className={'card-art ' + COLORES[i % COLORES.length]}>
                  <span>{ICONOS[g.categoria] || '✦'}</span>
                  <small>{g.categoria}</small>
                </div>
                <div className="card-body">
                  <div className="card-meta">
                    <span>{g.rango_edad}</span>
                    <span>Validado ✓</span>
                  </div>
                  <h3>{g.titulo}</h3>
                  <span className="card-cta">Ver guía →</span>
                </div>
              </article>
            ))}
          </div>
        )}

        {detalle && (
          <div className="modal-bg" onClick={() => setDetalle(null)}>
            <div className="perfil-detalle" onClick={(e) => e.stopPropagation()}>
              <header className="perfil-detalle-head">
                <div className="perfil-detalle-avatar" style={{ fontSize: 44 }} aria-hidden="true">
                  {ICONOS[detalle.categoria] || '✦'}
                </div>
                <div className="perfil-detalle-title">
                  <span className="eyebrow">{detalle.categoria?.toUpperCase()}</span>
                  <h2>{detalle.titulo}</h2>
                  <p>{detalle.rango_edad} años · Validado por profesionales</p>
                </div>
              </header>

              <div className="perfil-detalle-body" style={{ paddingTop: 20 }}>
                <section>
                  <h4>Contenido</h4>
                  <p>{detalle.contenido}</p>
                </section>
                {detalle.habitos_clave?.length > 0 && (
                  <section>
                    <h4>Hábitos clave</h4>
                    <div className="chips-inline">
                      {detalle.habitos_clave.map((h, i) => (
                        <span key={i} className="tag">{h}</span>
                      ))}
                    </div>
                  </section>
                )}
              </div>

              <div className="perfil-detalle-actions">
                <button className="btn-ghost" onClick={() => setDetalle(null)}>Cerrar</button>
                <button className="primary" onClick={() => setDetalle(null)}>Entendido</button>
              </div>
            </div>
          </div>
        )}
      </main>
    </>
  );
}
