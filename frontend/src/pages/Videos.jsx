import React, { useEffect, useState } from 'react';
import EmptyState from '../components/EmptyState';
import { videos as apiVideos } from '../api/client';

const GRUPOS = [
  { valor: '',      label: 'Todas',      emoji: '🎬' },
  { valor: '6-8',   label: '6-8 años',   emoji: '🧒' },
  { valor: '9-11',  label: '9-11 años',  emoji: '👦' },
  { valor: '12-14', label: '12-14 años', emoji: '🧑' },
];
const TINTE = { facil: 'sage', media: 'peach', dificil: 'sand' };
const DIF_LABEL = { facil: 'Fácil', media: 'Media', dificil: 'Difícil' };

function extraerId(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes('youtu.be')) return u.pathname.slice(1);
    return u.searchParams.get('v') || '';
  } catch { return ''; }
}

export default function Videos() {
  const [grupo, setGrupo] = useState('');
  const [items, setItems] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [detalle, setDetalle] = useState(null);

  useEffect(() => {
    setCargando(true); setError('');
    apiVideos.listar(grupo || undefined)
      .then((d) => setItems(Array.isArray(d) ? d : []))
      .catch((e) => setError(e.detail || e.message))
      .finally(() => setCargando(false));
  }, [grupo]);

  return (
    <>
      <main>
        {/* HERO glass marcado */}
        <section className="vid-hero">
          <div className="vid-hero-bg" aria-hidden="true" />
          <div className="vid-hero-content">
            <span className="eyebrow">BIBLIOTECA DE EJERCICIOS</span>
            <h1>Moverse es jugar.</h1>
            <p>Rutinas seguras por edad, con materiales y recomendaciones pensadas para cada etapa.</p>
          </div>
          <div className="vid-hero-stats">
            <div className="vid-stat">
              <span className="vid-stat-num">{items.length}</span>
              <span className="vid-stat-lbl">{grupo ? 'en este rango' : 'videos'}</span>
            </div>
            <div className="vid-stat">
              <span className="vid-stat-num">4</span>
              <span className="vid-stat-lbl">edades</span>
            </div>
            <div className="vid-stat">
              <span className="vid-stat-num">✓</span>
              <span className="vid-stat-lbl">seguros</span>
            </div>
          </div>
        </section>

        {error && <div className="notice warn">{error}</div>}

        {/* Filtros como chips glass */}
        <div className="vid-filtros">
          {GRUPOS.map((g) => (
            <button
              key={g.valor}
              type="button"
              className={'vid-chip' + (g.valor === grupo ? ' activo' : '')}
              onClick={() => setGrupo(g.valor)}
            >
              <span className="vid-chip-emoji">{g.emoji}</span>
              <span>{g.label}</span>
            </button>
          ))}
        </div>

        {cargando ? (
          <p>Cargando videos…</p>
        ) : items.length === 0 ? (
          <EmptyState icono="🎬" titulo="Sin videos" texto="Aún no hay videos en este rango." />
        ) : (
          <div className="vid-grid">
            {items.map((v) => (
              <article
                key={v.id}
                className={`vid-card vid-${TINTE[v.dificultad] || 'sage'}`}
                onClick={() => setDetalle(v)}
              >
                <div className="vid-card-glass" aria-hidden="true" />

                <header className="vid-card-head">
                  <span className="vid-badge">{DIF_LABEL[v.dificultad] || v.dificultad}</span>
                  <span className="vid-duracion">⏱ {Math.round(v.duracion_seg / 60)} min</span>
                </header>

                <div className="vid-card-art">
                  <div className="vid-art-circle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                      <polygon points="10 8 16 12 10 16 10 8" fill="currentColor"/>
                      <circle cx="12" cy="12" r="9"/>
                    </svg>
                  </div>
                </div>

                <div className="vid-card-body">
                  <span className="vid-edad">{v.grupo_edad} años</span>
                  <h3>{v.titulo}</h3>
                  <p>{v.descripcion}</p>
                  <div className="vid-card-foot">
                    <span className="vid-cta">
                      Ver detalle
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>
                      </svg>
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}

        {/* Detalle glass */}
        {detalle && (
          <div className="modal-bg" onClick={() => setDetalle(null)}>
            <div className={`vid-detalle vid-${TINTE[detalle.dificultad] || 'sage'}`} onClick={(e) => e.stopPropagation()}>
              <button className="vid-cerrar" onClick={() => setDetalle(null)} aria-label="Cerrar">✕</button>

              <header className="vid-detalle-head">
                <div className="vid-detalle-avatar">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
                    <polygon points="10 8 16 12 10 16 10 8" fill="currentColor"/>
                    <circle cx="12" cy="12" r="9"/>
                  </svg>
                </div>
                <div className="vid-detalle-info">
                  <div className="vid-detalle-chips">
                    <span className="vid-chip-tag">{detalle.grupo_edad} años</span>
                    <span className="vid-chip-tag">{DIF_LABEL[detalle.dificultad] || detalle.dificultad}</span>
                    <span className="vid-chip-tag">⏱ {Math.round(detalle.duracion_seg / 60)} min</span>
                  </div>
                  <h2>{detalle.titulo}</h2>
                </div>
              </header>

              <div className="vid-detalle-body">
                <section>
                  <h4>Descripción</h4>
                  <p>{detalle.descripcion}</p>
                </section>

                {detalle.materiales?.length > 0 && (
                  <section>
                    <h4>Materiales</h4>
                    <div className="chips-inline">
                      {detalle.materiales.map((m, i) => <span key={i} className="tag">{m}</span>)}
                    </div>
                  </section>
                )}

                {detalle.recomendaciones_seguridad?.length > 0 && (
                  <section>
                    <h4>Recomendaciones de seguridad</h4>
                    <ul className="lista-check">
                      {detalle.recomendaciones_seguridad.map((r, i) => <li key={i}>{r}</li>)}
                    </ul>
                  </section>
                )}

                {detalle.url_demo && (
                  <section>
                    <h4>Video</h4>
                    <div className="video-embed">
                      <iframe
                        src={`https://www.youtube.com/embed/${extraerId(detalle.url_demo)}`}
                        title={detalle.titulo}
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                      />
                    </div>
                  </section>
                )}
              </div>

              <div className="vid-detalle-actions">
                <button className="btn-ghost" onClick={() => setDetalle(null)}>Cerrar</button>
              </div>
            </div>
          </div>
        )}
      </main>
    </>
  );
}
