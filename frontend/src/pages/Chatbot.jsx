import React, { useEffect, useRef, useState } from 'react';
import { chatbot } from '../api/client';
import Markdown from '../components/Markdown';

const SUGERENCIAS = [
  '¿Qué merienda le puedo dar?',
  '¿Cuánta agua debe tomar al día?',
  'Ideas de cena saludable',
];

export default function Chatbot() {
  const [mensajes, setMensajes] = useState([
    { autor: 'bot', texto: 'Hola 👋 Soy el asistente nutricional de CreceActivo. Respondo solo con información validada. Si no tengo una respuesta segura, te derivo a un profesional.' },
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
      if (e.status === 503) setError('El chatbot no está configurado en el servidor.');
      else setError(e.detail || e.message);
    } finally { setCargando(false); }
  }

  return (
    <>
      <main>
        <div className="page-head">
          <div>
            <h1>Asistente nutricional</h1>
            <p>Respondo con información validada. Nunca doy diagnósticos.</p>
          </div>
          <span className="pill-live"><i /> En línea</span>
        </div>

        {error && <div className="notice warn">{error}</div>}

        <section className="chat-shell">
          <div className="chat-log">
            {mensajes.map((m, i) => (
              <div key={i} className={`bubble-row ${m.autor}`}>
                {m.autor === 'bot' && <span className="bubble-avatar">✦</span>}
                <div className={`bubble ${m.autor}`}>
                  {m.autor === 'bot' ? <Markdown>{m.texto}</Markdown> : m.texto}
                </div>
              </div>
            ))}
            {cargando && (
              <div className="bubble-row bot">
                <span className="bubble-avatar">✦</span>
                <div className="bubble bot typing"><span/><span/><span/></div>
              </div>
            )}
            <div ref={fin} />
          </div>

          <div className="chat-sugerencias">
            {SUGERENCIAS.map((s) => (
              <button key={s} className="chip" onClick={() => enviar(s)} disabled={cargando}>
                {s}
              </button>
            ))}
          </div>

          <form className="chat-input" onSubmit={(e) => { e.preventDefault(); enviar(); }}>
            <input
              type="text" value={texto} onChange={(e) => setTexto(e.target.value)}
              placeholder="Escribe tu pregunta…" disabled={cargando}
            />
            <button type="submit" className="primary" disabled={cargando || !texto.trim()}>
              {cargando ? '…' : 'Enviar'}
            </button>
          </form>
        </section>
      </main>
    </>
  );
}
