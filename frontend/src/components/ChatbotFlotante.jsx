// Asistente flotante. Responde preguntas basicas localmente y
// deriva al backend (Gemini) para consultas nutricionales.
import React, { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { chatbot } from '../api/client';
import Markdown from './Markdown';

const BASICAS = [
  { k: ['hola', 'buenas', 'hey', 'hi'], a: '¡Hola! 👋 Soy **Crece**. Puedo responder dudas básicas de CreceActivo o consultas de nutrición. ¿En qué te ayudo?' },
  { k: ['gracias', 'thank'], a: '¡De nada! 💚 Cuando necesites algo, aquí estoy.' },
  { k: ['quien eres', 'quién eres', 'que eres', 'qué eres'], a: 'Soy **Crece**, el asistente de CreceActivo. Respondo dudas básicas sobre la plataforma y consultas de nutrición infantil validadas.' },
  { k: ['que es creceactivo', 'qué es creceactivo'], a: '**CreceActivo** es una plataforma para familias que previene el sedentarismo y la obesidad infantil en niños de 6 a 14 años, con guías, videos y seguimiento.' },
  { k: ['crear perfil', 'agregar hijo', 'agregar perfil', 'nuevo perfil', 'registrar hijo', 'creo un perfil'], a: 'Ve a **Mis hijos** en el menú lateral y toca **+ Agregar hijo/a**. Completa los datos y guarda.' },
  { k: ['imc', 'calcular imc', 'indice masa'], a: 'Ve a **IMC orientativo**, elige un perfil y toca **Calcular IMC**. Verás el resultado y su ubicación según la OMS.' },
  { k: ['videos', 'ejercicios', 'rutinas'], a: 'En **Videos** encuentras rutinas clasificadas por edad (6-8, 9-11, 12-14) con materiales y recomendaciones de seguridad.' },
  { k: ['progreso', 'racha', 'insignia', 'meta'], a: 'En **Progreso** registras agua, minutos activos y rutinas. Ahí ves rachas, insignias y metas familiares.' },
  { k: ['ayuda', 'help'], a: 'Puedo ayudarte con: crear un perfil, calcular IMC, ver videos, revisar progreso y dudas básicas de nutrición. Prueba con *"¿cómo creo un perfil?"*' },
];

function responderBasica(pregunta) {
  const q = pregunta.toLowerCase().trim();
  for (const item of BASICAS) if (item.k.some((k) => q.includes(k))) return item.a;
  return null;
}

const SUGERENCIAS = ['¿Cómo creo un perfil?', '¿Cómo veo el IMC?', '¿Qué son las insignias?'];

export default function ChatbotFlotante() {
  const { pathname } = useLocation();
  const oculto = pathname === '/chatbot';
  const [abierto, setAbierto] = useState(false);
  const [mensajes, setMensajes] = useState([
    { autor: 'bot', texto: '¡Hola! 👋 Soy **Crece**. Puedo responder dudas básicas o consultas de nutrición. ¿Qué necesitas?' },
  ]);
  const [texto, setTexto] = useState('');
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');
  const fin = useRef(null);

  useEffect(() => {
    if (abierto && fin.current) fin.current.scrollIntoView({ behavior: 'smooth' });
  }, [mensajes, abierto]);

  async function enviar(pregunta) {
    const p = (pregunta ?? texto).trim();
    if (!p || cargando) return;
    setError('');
    setMensajes((m) => [...m, { autor: 'user', texto: p }]);
    setTexto('');

    const basica = responderBasica(p);
    if (basica) {
      setTimeout(() => setMensajes((m) => [...m, { autor: 'bot', texto: basica }]), 220);
      return;
    }

    setCargando(true);
    try {
      const r = await chatbot.preguntar(p);
      setMensajes((m) => [...m, { autor: 'bot', texto: r.respuesta }]);
    } catch (e) {
      const msg = e.status === 503
        ? 'El asistente está saturado. Prueba en unos segundos.'
        : e.status === 401
        ? 'Vuelve a iniciar sesión.'
        : 'No pude conectar. Intenta más tarde.';
      setError(msg);
    } finally { setCargando(false); }
  }

  if (oculto) return null;

  return (
    <>
      {!abierto && (
        <button className="cf-boton" onClick={() => setAbierto(true)} aria-label="Abrir asistente">
          <img src="/ilustraciones/nino.png" alt="" />
          <span className="cf-punto" />
        </button>
      )}

      {abierto && (
        <div className="cf-panel" role="dialog" aria-label="Asistente Crece">
          <header className="cf-head">
            <img src="/ilustraciones/nino.png" alt="" className="cf-avatar" />
            <div>
              <strong>Crece</strong>
              <span className="cf-estado"><i /> En línea</span>
            </div>
            <button className="cf-cerrar" onClick={() => setAbierto(false)} aria-label="Cerrar">✕</button>
          </header>

          <div className="cf-log">
            {mensajes.map((m, i) => (
              <div key={i} className={`cf-bubble-row ${m.autor}`}>
                {m.autor === 'bot' && <span className="cf-avatar-mini">✳</span>}
                <div className={`cf-bubble ${m.autor}`}>
                  {m.autor === 'bot' ? <Markdown>{m.texto}</Markdown> : m.texto}
                </div>
              </div>
            ))}
            {cargando && (
              <div className="cf-bubble-row bot">
                <span className="cf-avatar-mini">✳</span>
                <div className="cf-bubble bot typing"><span/><span/><span/></div>
              </div>
            )}
            {error && <div className="cf-error">{error}</div>}
            <div ref={fin} />
          </div>

          {mensajes.length <= 1 && (
            <div className="cf-sugerencias">
              {SUGERENCIAS.map((s) => (
                <button key={s} className="chip" onClick={() => enviar(s)}>{s}</button>
              ))}
            </div>
          )}

          <form className="cf-input" onSubmit={(e) => { e.preventDefault(); enviar(); }}>
            <input
              type="text" value={texto} onChange={(e) => setTexto(e.target.value)}
              placeholder="Escribe tu pregunta…" disabled={cargando}
            />
            <button type="submit" disabled={cargando || !texto.trim()} aria-label="Enviar">➤</button>
          </form>
        </div>
      )}
    </>
  );
}
