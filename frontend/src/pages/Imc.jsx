// Modulo 2: IMC orientativo con percentiles OMS.
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import EmptyState from '../components/EmptyState';
import { perfiles as apiPerfiles, imc as apiImc } from '../api/client';

const COLORES = {
  bajo: 'sky',
  adecuado: 'sage',
  alto: 'peach',
  muy_alto: 'sand',
};

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
    try {
      setResultado(await apiImc.calcular(perfilId));
    } catch (e) {
      setError(e.detail || e.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <>
      <Header titulo="IMC orientativo" />
      <main>
        <section className="hero small">
          <div>
            <span className="eyebrow">REFERENCIA, NO DIAGNOSTICO</span>
            <h1>Una guia,{'\n'}no una etiqueta.</h1>
            <p>Calculamos el IMC del perfil y lo ubicamos según tablas OMS 5-19 años.</p>
          </div>
        </section>

        {error && <div className="notice warn">{error}</div>}

        {hijos.length === 0 && !error ? (
          <EmptyState
            titulo="Aún no hay perfiles"
            texto="Crea un perfil infantil antes de calcular su IMC."
          />
        ) : (
          <section className="card">
            <div className="filters">
              <label>Perfil
                <select value={perfilId} onChange={(e) => setPerfilId(e.target.value)}>
                  {hijos.map((h) => (
                    <option key={h.id} value={h.id}>{h.nombre}</option>
                  ))}
                </select>
              </label>
            </div>
            <button onClick={calcular} disabled={cargando || !perfilId}>
              {cargando ? 'Calculando...' : 'Calcular IMC'}
            </button>
          </section>
        )}

        {resultado && (
          <section className={`card ${COLORES[resultado.categoria] || 'sage'}`}>
            <span className="eyebrow">RESULTADO ORIENTATIVO</span>
            <h2>IMC {resultado.imc}</h2>
            <p>Puntaje z: <strong>{resultado.z}</strong></p>
            <p>Categoría: <strong>{resultado.categoria.replace('_', ' ')}</strong></p>
            <p className="notice">{resultado.aviso}</p>
          </section>
        )}
      </main>
    </>
  );
}
