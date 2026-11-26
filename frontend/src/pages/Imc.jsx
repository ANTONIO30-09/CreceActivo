import React, { useEffect, useState } from 'react';
import EmptyState from '../components/EmptyState';
import { perfiles as apiPerfiles, imc as apiImc } from '../api/client';

const CAT_INFO = {
  bajo:      { label: 'Bajo',     color: '#38bdf8', emoji: '🌊', texto: 'Por debajo de lo esperado para su edad.' },
  adecuado:  { label: 'Adecuado', color: '#10b981', emoji: '🌿', texto: 'En rango saludable para su edad.' },
  alto:      { label: 'Alto',     color: '#f59e0b', emoji: '🌤', texto: 'Por encima de lo esperado para su edad.' },
  muy_alto:  { label: 'Muy alto', color: '#ef4444', emoji: '🔥', texto: 'Muy por encima de lo esperado. Conviene consultar.' },
};

function avatarDe(p) {
  return p?.sexo === 'femenino' ? '/ilustraciones/nina.png' : '/ilustraciones/nino.png';
}

export default function Imc() {
  const [hijos, setHijos] = useState([]);
  const [perfilId, setPerfilId] = useState('');
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    apiPerfiles.listar()
      .then((d) => {
        const lista = Array.isArray(d) ? d : [];
        setHijos(lista);
        if (lista[0]) setPerfilId(lista[0].id);
      })
      .catch((e) => setError(e.detail || e.message));
  }, []);

  async function calcular() {
    if (!perfilId) return;
    setCargando(true); setError(''); setResultado(null);
    try { setResultado(await apiImc.calcular(perfilId)); }
    catch (e) { setError(e.detail || e.message); }
    finally { setCargando(false); }
  }

  const perfilSel = hijos.find((h) => h.id === perfilId);
  const cat = resultado ? (CAT_INFO[resultado.categoria] || CAT_INFO.adecuado) : null;

  return (
    <>
      <main>
        <div className="page-head">
          <div>
            <h1>IMC orientativo</h1>
            <p>Referencia según tablas OMS 5-19 años. Nunca es un diagnóstico.</p>
          </div>
        </div>

        {error && <div className="notice warn">{error}</div>}

        {hijos.length === 0 && !error ? (
          <EmptyState
            imagen="/ilustraciones/nino-nina.png"
            titulo="Aún no hay perfiles"
            texto="Crea un perfil infantil antes de calcular su IMC."
          />
        ) : (
          <div className="imc-layout">
            {/* ============ Columna izquierda: selección ============ */}
            <section className="imc-panel">
              <header className="imc-panel-head">
                <span className="eyebrow">PASO 1</span>
                <h2>Elige el perfil</h2>
                <p>Usaremos sus datos de edad, sexo, peso y estatura.</p>
              </header>

              <div className="imc-perfiles">
                {hijos.map((h) => (
                  <button
                    key={h.id}
                    type="button"
                    className={'imc-perfil' + (h.id === perfilId ? ' activo' : '')}
                    onClick={() => { setPerfilId(h.id); setResultado(null); }}
                  >
                    <div>
                      <strong>{h.nombre}</strong>
                      <span>{h.edad} años · {h.peso_kg} kg · {h.estatura_cm} cm</span>
                    </div>
                  </button>
                ))}
              </div>

              <button
                className="primary imc-btn"
                onClick={calcular}
                disabled={cargando || !perfilId}
              >
                {cargando ? 'Calculando…' : 'Calcular IMC →'}
              </button>

              <div className="imc-aviso-panel">
                <span className="imc-aviso-ico">i</span>
                <p>
                  El IMC es una referencia general. No etiqueta al niño/a ni
                  reemplaza la evaluación de un profesional.
                </p>
              </div>
            </section>

            {/* ============ Columna derecha: resultado ============ */}
            <section className="imc-resultado-col">
              {!resultado ? (
                <div className="imc-placeholder">
                  <div className="imc-placeholder-icon">📏</div>
                  <h3>Tu resultado aparecerá aquí</h3>
                  <p>Selecciona un perfil y pulsa "Calcular IMC".</p>
                </div>
              ) : (
                <article className="imc-resultado-card" style={{ '--accent': cat.color }}>
                  <header className="imc-res-head">
                    {perfilSel && (
                      <div className="imc-res-avatar">
                        <img src={avatarDe(perfilSel)} alt="" />
                      </div>
                    )}
                    <div className="imc-res-info">
                      <span className="eyebrow">RESULTADO ORIENTATIVO</span>
                      <h2>{perfilSel?.nombre}</h2>
                      <p>{perfilSel?.edad} años · {perfilSel?.sexo}</p>
                    </div>
                  </header>

                  <div className="imc-res-numero">
                    <span className="imc-res-label">IMC</span>
                    <span className="imc-res-value">{resultado.imc}</span>
                  </div>
                  <div className="imc-res-z-info">
                    <div className="imc-res-z-head">
                      <span className="imc-res-z-emoji" aria-hidden="true">📊</span>
                      <strong>Comparación con niños de su edad</strong>
                    </div>
                    <p>
                      Este número indica qué tan lejos está {perfilSel?.nombre || 'el niño/a'} del
                      promedio de otros niños de su misma edad y sexo. Cuanto más cerca de <strong>0</strong>,
                      más cerca del promedio. Un resultado entre <strong>−2 y +2</strong> se considera
                      dentro de lo esperado.
                    </p>
                    <span className="imc-res-z-valor">Valor actual: {resultado.z}</span>
                  </div>

                  <div className="imc-res-categoria" style={{ background: `${cat.color}22`, borderColor: `${cat.color}66` }}>
                    <span className="imc-cat-emoji">{cat.emoji}</span>
                    <div>
                      <strong style={{ color: cat.color }}>{cat.label}</strong>
                      <p>{cat.texto}</p>
                    </div>
                  </div>

                  <div className="imc-escala">
                    <div className="imc-escala-head">
                      <span className="imc-escala-titulo">📍 Dónde se ubica</span>
                      <span className="imc-escala-sub">Comparado con niños de su edad</span>
                    </div>
                    <div className="imc-escala-barra">
                      <span className="imc-tramo bajo" />
                      <span className="imc-tramo adecuado" />
                      <span className="imc-tramo alto" />
                      <span className="imc-tramo muy" />
                      <span
                        className="imc-marcador"
                        style={{
                          left: `${Math.min(96, Math.max(4, 50 + (resultado.z * 12)))}%`,
                          background: cat.color,
                        }}
                      >
                        <span className="imc-marcador-label">Aquí está {perfilSel?.nombre || ''}</span>
                      </span>
                    </div>
                    <div className="imc-escala-etiq">
                      <span><strong>Bajo</strong><small>Menos de lo esperado</small></span>
                      <span><strong>Saludable</strong><small>Dentro de lo esperado</small></span>
                      <span><strong>Alto</strong><small>Más de lo esperado</small></span>
                      <span><strong>Muy alto</strong><small>Conviene consultar</small></span>
                    </div>
                  </div>

                  <div className="imc-aviso-final">
                    <span className="imc-aviso-final-ico" aria-hidden="true">💡</span>
                    <p>{resultado.aviso}</p>
                  </div>
                </article>
              )}
            </section>
          </div>
        )}
      </main>
    </>
  );
}
