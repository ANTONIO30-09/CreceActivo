import React, { useEffect, useMemo, useState } from 'react';
import EmptyState from '../components/EmptyState';
import { nutricion } from '../api/client';

const RANGOS = [
  { v: '',      l: 'Todas' },
  { v: '6-8',   l: '6-8' },
  { v: '9-11',  l: '9-11' },
  { v: '12-14', l: '12-14' },
];
const CATS = [
  { v: '',              l: 'Todas',        ico: '✦' },
  { v: 'Habitos',       l: 'Hábitos',      ico: '✦' },
  { v: 'Meriendas',     l: 'Meriendas',    ico: '◒' },
  { v: 'Alimentacion',  l: 'Alimentación', ico: '◇' },
];
const ICONOS = { Habitos: '✦', Meriendas: '◒', Alimentacion: '◇' };
const TINTES = { Habitos: 'sage', Meriendas: 'peach', Alimentacion: 'violet' };

export default function Nutricion() {
  const [guias, setGuias] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [cat, setCat] = useState('');
  const [edad, setEdad] = useState('');
  const [detalle, setDetalle] = useState(null);

  useEffect(() => {
    setCargando(true); setError('');
    nutricion.guias()
      .then((d) => setGuias(Array.isArray(d) ? d : []))
      .catch((e) => setError(e.detail || e.message))
      .finally(() => setCargando(false));
  }, []);

  const visibles = useMemo(() => {
    const q = query.trim().toLowerCase();
    return guias.filter((g) => {
      const okQ = !q || g.titulo.toLowerCase().includes(q) || g.contenido.toLowerCase().includes(q);
      const okC = !cat || g.categoria === cat;
      const okE = !edad || g.rango_edad === edad;
      return okQ && okC && okE;
    });
  }, [guias, query, cat, edad]);

  const destacada = visibles[0];
  const resto = visibles.slice(1);

  return (
    <>
      <main>
        {/* Masthead */}
        <header className="nut-masthead">
          <div className="nut-masthead-txt">
            <span className="nut-kicker">NUTRICIÓN · CRECE ACTIVO</span>
            <h1>Guías para crecer</h1>
            <p>Contenido validado por profesionales de la nutrición infantil.</p>
          </div>
          <div className="nut-search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>
            </svg>
            <input
              type="search" value={query} onChange={(e) => setQuery(e.target.value)}
              placeholder="Buscar por título o tema…"
            />
          </div>
        </header>

        {/* Filtros */}
        <div className="nut-filtros">
          <div className="nut-filtros-group">
            <span className="nut-filtros-lbl">Categoría</span>
            {CATS.map((c) => (
              <button
                key={c.v}
                className={'nut-pill' + (c.v === cat ? ' activo' : '')}
                onClick={() => setCat(c.v)}
              >
                <span className="nut-pill-ico">{c.ico}</span>{c.l}
              </button>
            ))}
          </div>
          <div className="nut-filtros-group">
            <span className="nut-filtros-lbl">Edad</span>
            {RANGOS.map((r) => (
              <button
                key={r.v}
                className={'nut-pill nut-pill-age' + (r.v === edad ? ' activo' : '')}
                onClick={() => setEdad(r.v)}
              >
                {r.l}{r.v ? ' años' : ''}
              </button>
            ))}
          </div>
        </div>

        {error && <div className="notice warn">No se pudo conectar con el backend.</div>}
        {cargando && <p>Cargando guías…</p>}

        {!cargando && visibles.length === 0 && (
          <EmptyState
            icono="🥗"
            titulo="Sin resultados"
            texto={error ? 'Revisa la conexión con el backend.' : 'Prueba con otro filtro o búsqueda.'}
          />
        )}

        {!cargando && visibles.length > 0 && (
          <>
            {/* Destacada */}
            <section className="nut-destacada">
              <article
                className={`nut-feat nut-feat-${TINTES[destacada.categoria] || 'sage'}`}
                onClick={() => setDetalle(destacada)}
              >
                <div className="nut-feat-art" aria-hidden="true">
                  <span>{ICONOS[destacada.categoria] || '✦'}</span>
                </div>
                <div className="nut-feat-body">
                  <div className="nut-feat-tags">
                    <span className="nut-tag">{destacada.categoria}</span>
                    <span className="nut-tag nut-tag-lite">{destacada.rango_edad} años</span>
                    <span className="nut-tag nut-tag-ok">✓ Validado</span>
                  </div>
                  <h2>{destacada.titulo}</h2>
                  <p>{destacada.contenido}</p>
                  <div className="nut-feat-foot">
                    <span className="nut-leer">
                      Leer guía
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
                      </svg>
                    </span>
                    <span className="nut-tiempo">⏱ {Math.max(2, Math.round((destacada.contenido?.length || 0) / 120))} min</span>
                  </div>
                </div>
              </article>

              <aside className="nut-side">
                <span className="nut-side-lbl">También para ti</span>
                {resto.slice(0, 3).map((g) => (
                  <article
                    key={g.id}
                    className={`nut-mini nut-mini-${TINTES[g.categoria] || 'sage'}`}
                    onClick={() => setDetalle(g)}
                  >
                    <div className="nut-mini-ico">{ICONOS[g.categoria] || '✦'}</div>
                    <div className="nut-mini-info">
                      <span className="nut-mini-cat">{g.categoria} · {g.rango_edad}</span>
                      <h4>{g.titulo}</h4>
                    </div>
                    <svg className="nut-mini-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
                    </svg>
                  </article>
                ))}
                {resto.length === 0 && (
                  <div className="nut-side-empty">Más guías en camino ✨</div>
                )}
              </aside>
            </section>

            {/* Resto en lista editorial */}
            {resto.length > 3 && (
              <section className="nut-resto">
                <header className="nut-resto-head">
                  <h3>Más guías</h3>
                  <span>{resto.length - 3} artículos</span>
                </header>
                <div className="nut-row-list">
                  {resto.slice(3).map((g) => (
                    <article
                      key={g.id}
                      className={`nut-row nut-row-${TINTES[g.categoria] || 'sage'}`}
                      onClick={() => setDetalle(g)}
                    >
                      <div className="nut-row-ico">{ICONOS[g.categoria] || '✦'}</div>
                      <div className="nut-row-txt">
                        <span className="nut-row-cat">{g.categoria} · {g.rango_edad} años</span>
                        <h4>{g.titulo}</h4>
                        <p>{g.contenido}</p>
                      </div>
                      <div className="nut-row-meta">
                        <span>{Math.max(2, Math.round((g.contenido?.length || 0) / 120))} min</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
                        </svg>
                      </div>
                    </article>
                  ))}
                </div>
              </section>
            )}
          </>
        )}

        {/* Detalle (mantenido) */}
        {detalle && (
          <div className="modal-bg" onClick={() => setDetalle(null)}>
            <div className="guia-detalle" onClick={(e) => e.stopPropagation()}>
              <button className="guia-cerrar" onClick={() => setDetalle(null)} aria-label="Cerrar">✕</button>

              <header className="guia-hero">
                <div className="guia-hero-icon" aria-hidden="true">
                  {ICONOS[detalle.categoria] || '✦'}
                </div>
                <div className="guia-hero-texto">
                  <span className="eyebrow">{detalle.categoria?.toUpperCase()}</span>
                  <h1>{detalle.titulo}</h1>
                  <div className="guia-meta">
                    <span className="guia-chip">👶 {detalle.rango_edad} años</span>
                    <span className="guia-chip">✓ Validado por profesionales</span>
                    <span className="guia-chip">📖 {Math.max(2, Math.round((detalle.contenido?.length || 0) / 120))} min</span>
                  </div>
                </div>
              </header>

              <div className="guia-cuerpo">
                <article className="guia-main">
                  <section className="guia-bloque">
                    <h3>¿De qué se trata?</h3>
                    <p className="guia-lead">{detalle.contenido}</p>
                  </section>
                  {detalle.habitos_clave?.length > 0 && (
                    <section className="guia-bloque">
                      <h3>Hábitos clave</h3>
                      <p className="guia-hint">Intenta incorporarlos de a uno por semana. La constancia importa más que la velocidad.</p>
                      <ul className="guia-habitos">
                        {detalle.habitos_clave.map((h, i) => (
                          <li key={i}><span className="guia-check">✓</span><span>{h}</span></li>
                        ))}
                      </ul>
                    </section>
                  )}
                  <section className="guia-bloque">
                    <h3>Cómo ponerlo en práctica</h3>
                    <ol className="guia-pasos">
                      <li>Elige un hábito de la lista y coméntenlo en familia esta semana.</li>
                      <li>Anoten el progreso a diario en la sección Progreso del perfil.</li>
                      <li>Al cerrar la semana, celebren el logro y sumen un hábito nuevo.</li>
                      <li>Si algo no funciona, ajusten sin culpa y vuelvan a intentarlo.</li>
                    </ol>
                  </section>
                  <section className="guia-bloque">
                    <h3>Ten en cuenta</h3>
                    <p className="guia-lead">Cada niño/a es distinto. Si notas cambios bruscos de peso, apetito o ánimo, consulta con un profesional de la salud. Esta guía es educativa y no reemplaza la consulta médica.</p>
                  </section>
                </article>
                <aside className="guia-side">
                  <div className="guia-side-card"><span className="guia-side-label">Categoría</span><span className="guia-side-value">{detalle.categoria}</span></div>
                  <div className="guia-side-card"><span className="guia-side-label">Rango de edad</span><span className="guia-side-value">{detalle.rango_edad} años</span></div>
                  <div className="guia-side-card"><span className="guia-side-label">Validación</span><span className="guia-side-value">Profesional</span></div>
                  <div className="guia-side-aviso"><strong>Recuerda:</strong> ante cualquier duda específica, consulta con un nutricionista o pediatra.</div>
                </aside>
              </div>

              <div className="guia-footer">
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
