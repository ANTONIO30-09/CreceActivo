// Modulo 2: chatbot que solo responde con informacion validada.
import React, { useEffect, useRef, useState } from 'react';
import Header from '../components/Header';
import { chatbot } from '../api/client';

const SUGERENCIAS = [
  '¿Qué merienda le puedo dar?',
  '¿Cuánta agua debe tomar al día?',
  'Ideas de cena saludable',
];

export default function Chatbot() {
  const [mensajes, setMensajes] = useState([
    { autor: 'bot', texto: 'Hola. Puedo ayudarte con información sobre alimentación infantil validada por profesionales. ¿Qué necesitas?' },
  ]);
  const [texto, setTexto] = useState('');
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');
  const fin = useRef(null);

  useEffect(() => { fin.current?.scrollIntoView({ behavior: 'smooth' }); }, [mensajes]);

  async function enviar(pregunta) {
    const p = (pregunta ?? texto).trim();
    if (!p || cargando) return;
    setError('');
    setMensajes((m) => [...m, { autor: 'user', texto: p }]);
    setTexto('');
    setCargando(true);
    try {
      const r = await chatbot.preguntar(p);
      setMensajes((m) => [...m, { autor: 'bot', texto: r.respuesta }]);
    } catch (e) {
      if (e.status === 503) {
        setError('El chatbot no está configurado en el servidor.');
      } else {
        setError(e.detail || e.message);
      }
    } finally {
      setCargando(false);
    }
  }

  return (
    <>
      <Header titulo="Chatbot nutricional" />
      <main>
        <section className="hero small">
          <div>
            <span className="eyebrow">SOLO INFORMACION VALIDADA</span>
            <h1>Pregunta sin miedo.</h1>
            <p>Si no tengo una respuesta segura, te derivo a un profesional.</p>
          </div>
        </section>

        {error && <div className="notice warn">{error}</div>}

        <section className="card">
          <div className="chat-log">
            {mensajes.map((m, i) => (
              <div key={i} className={`bubble ${m.autor}`}>{m.texto}</div>
            ))}
            {cargando && <div className="bubble bot">Escribiendo...</div>}
            <div ref={fin} />
          </div>

          <div className="filters">
            {SUGERENCIAS.map((s) => (
              <button key={s} className="chip" onClick={() => enviar(s)} disabled={cargando}>
                {s}
              </button>
            ))}
          </div>

          <form
            onSubmit={(e) => { e.preventDefault(); enviar(); }}
            style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}
          >
            <input
              type="text"
              value={texto}
              onChange={(e) => setTexto(e.target.value)}
              placeholder="Escribe tu pregunta..."
              disabled={cargando}
              style={{ flex: 1 }}
            />
            <button type="submit" disabled={cargando || !texto.trim()}>Enviar</button>
          </form>
        </section>
      </main>
    </>
  );
}
