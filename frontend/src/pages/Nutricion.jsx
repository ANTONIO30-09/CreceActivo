// Modulo 2: guias y menus conectados al backend real.
import React, { useEffect, useMemo, useState } from 'react';
import Header from '../components/Header';
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
      <Header titulo="Nutricion y orientacion profesional" />
      <main>
        <section className="hero small">
          <div>
            <span className="eyebrow">CRECER JUNTOS</span>
            <h1>Pequeños hábitos.{'\n'}Grandes comienzos.</h1>
            <p>Guías y menús validados por profesionales de la nutrición.</p>
          </div>
        </section>

        {error && (
          <div className="notice warn">
            No se pudo conectar con el backend. Verifica que esté corriendo en{' '}
            <code>localhost:8000</code>.
          </div>
        )}

        <div className="section-heading">
          <div>
            <h2>Guías para tu familia</h2>
            <p>Encuentra contenido por tema y rango de edad.</p>
          </div>
          <span>{visibles.length} resultados</span>
        </div>

        <div className="filters">
          <label>Buscar guía
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Escribe un título..."
            />
          </label>
          <label>Rango de edad
            <select value={edad} onChange={(e) => setEdad(e.target.value)}>
              {RANGOS.map((r) => <option key={r}>{r}</option>)}
            </select>
          </label>
        </div>

        {cargando && <p>Cargando guias...</p>}

        {!cargando && visibles.length === 0 && (
          <EmptyState
            icono="🥗"
            titulo="No hay guías disponibles"
            texto={error ? 'Revisa la conexión con el backend.' : 'Prueba con otro filtro.'}
          />
        )}

        {detalle ? (
          <section className="detail">
            <button className="text-button" onClick={() => setDetalle(null)}>← Volver al catálogo</button>
            <p className="eyebrow">{detalle.categoria} · {detalle.rango_edad}</p>
            <h2>{detalle.titulo}</h2>
            <p>{detalle.contenido}</p>
            <h3>Habitos clave</h3>
            <ul>{(detalle.habitos_clave || []).map((h) => <li key={h}>{h}</li>)}</ul>
          </section>
        ) : (
          !cargando && visibles.length > 0 && (
            <div className="cards">
              {visibles.map((g, i) => (
                <article key={g.id} className="card">
                  <div className={'card-art ' + COLORES[i % COLORES.length]}>
                    <span>{ICONOS[g.categoria] || '✦'}</span>
                    <small>{g.categoria}</small>
                  </div>
                  <div className="card-body">
                    <div className="card-meta">
                      <span>{g.rango_edad}</span>
                      <span>Validado</span>
                    </div>
                    <h3>{g.titulo}</h3>
                    <button onClick={() => setDetalle(g)}>Ver guía →</button>
                  </div>
                </article>
              ))}
            </div>
          )
        )}
      </main>
    </>
  );
}
