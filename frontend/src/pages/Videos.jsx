// Modulo 3: biblioteca de videos por rango de edad.
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import EmptyState from '../components/EmptyState';
import { videos as apiVideos } from '../api/client';

const GRUPOS = [
  { valor: '', label: 'Todas las edades' },
  { valor: '6-8', label: '6-8 años' },
  { valor: '9-11', label: '9-11 años' },
  { valor: '12-14', label: '12-14 años' },
];

const DIFICULTAD_COLOR = { facil: 'sage', media: 'peach', dificil: 'sand' };

export default function Videos() {
  const [grupo, setGrupo] = useState('');
  const [items, setItems] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    setCargando(true); setError('');
    apiVideos.listar(grupo || undefined)
      .then((d) => setItems(Array.isArray(d) ? d : []))
      .catch((e) => setError(e.detail || e.message))
      .finally(() => setCargando(false));
  }, [grupo]);

  return (
    <>
      <Header titulo="Biblioteca de videos" />
      <main>
        <section className="hero small">
          <div>
            <span className="eyebrow">EJERCICIO EN FAMILIA</span>
            <h1>Moverse es jugar.</h1>
            <p>Videos clasificados por edad, con materiales y recomendaciones de seguridad.</p>
          </div>
        </section>

        {error && <div className="notice warn">{error}</div>}

        <div className="filters">
          <label>Rango de edad
            <select value={grupo} onChange={(e) => setGrupo(e.target.value)}>
              {GRUPOS.map((g) => <option key={g.valor} value={g.valor}>{g.label}</option>)}
            </select>
          </label>
          <span>{items.length} videos</span>
        </div>

        {cargando ? (
          <p>Cargando videos...</p>
        ) : items.length === 0 ? (
          <EmptyState titulo="Sin videos" texto="Aún no hay videos en este rango." />
        ) : (
          <div className="grid">
            {items.map((v) => (
              <article key={v.id} className={`card ${DIFICULTAD_COLOR[v.dificultad] || 'sage'}`}>
                <span className="eyebrow">{v.grupo_edad} años · {v.dificultad}</span>
                <h3>{v.titulo}</h3>
                <p>{v.descripcion}</p>
                <p><strong>Duración:</strong> {Math.round(v.duracion_seg / 60)} min</p>
                {v.materiales.length > 0 && (
                  <p><strong>Materiales:</strong> {v.materiales.join(', ')}</p>
                )}
                {v.recomendaciones_seguridad.length > 0 && (
                  <ul>
                    {v.recomendaciones_seguridad.map((r, i) => <li key={i}>{r}</li>)}
                  </ul>
                )}
              </article>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
