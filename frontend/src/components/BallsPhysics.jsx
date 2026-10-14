// Pelotas que viajan por la pantalla, rebotan en los bordes,
// se pueden agarrar/lanzar y muestran "+1".
import React, { useEffect, useRef } from 'react';

const BALLS = [
  { src: '/balls/futbol.png' }, { src: '/balls/futbol.png' }, { src: '/balls/futbol.png' },
  { src: '/balls/basquet.png' }, { src: '/balls/basquet.png' }, { src: '/balls/basquet.png' },
  { src: '/balls/tenis.png' },   { src: '/balls/tenis.png' },   { src: '/balls/tenis.png' },
  { src: '/balls/valley.png' },  { src: '/balls/valley.png' },  { src: '/balls/valley.png' },
];
const SIZE = 120;
const CRUISE = 1.6;       // velocidad "de viaje" a la que siempre vuelven
const WALL_BOUNCE = 0.92; // pérdida de energía al chocar con pared
const DECAY = 0.985;      // cuánto baja la velocidad extra cada frame

export default function BallsPhysics() {
  const layerRef = useRef(null);
  const ballsRef = useRef([]);

  useEffect(() => {
    const layer = layerRef.current;
    if (!layer) return;
    const W = () => window.innerWidth;
    const H = () => window.innerHeight;

    const state = BALLS.map(() => ({
      x: Math.random() * Math.max(1, W() - SIZE),
      y: Math.random() * Math.max(1, H() - SIZE),
      vx: CRUISE * (Math.random() < 0.5 ? -1 : 1) * (0.9 + Math.random() * 0.3),
      vy: CRUISE * (Math.random() < 0.5 ? -1 : 1) * (0.9 + Math.random() * 0.3),
      dragging: false, gx: 0, gy: 0, lx: 0, ly: 0, lt: 0,
    }));

    let dragIdx = -1;

    const onDown = (e) => {
      const i = ballsRef.current.indexOf(e.target);
      if (i < 0) return;
      dragIdx = i;
      const s = state[i];
      s.dragging = true;
      s.gx = e.clientX - s.x;
      s.gy = e.clientY - s.y;
      s.lx = e.clientX; s.ly = e.clientY; s.lt = performance.now();
      s.vx = 0; s.vy = 0;
      e.preventDefault();
    };

    const onMove = (e) => {
      if (dragIdx < 0) return;
      const s = state[dragIdx];
      const now = performance.now();
      const dt = Math.max(8, now - s.lt);
      s.vx = ((e.clientX - s.lx) / dt) * 16;
      s.vy = ((e.clientY - s.ly) / dt) * 16;
      s.x = e.clientX - s.gx;
      s.y = e.clientY - s.gy;
      s.lx = e.clientX; s.ly = e.clientY; s.lt = now;
    };

    const onUp = () => {
      if (dragIdx < 0) return;
      const s = state[dragIdx];
      s.dragging = false;
      const sp = Math.hypot(s.vx, s.vy);
      const MAX = 14, MIN = 2.0;
      if (sp > MAX) { s.vx = s.vx / sp * MAX; s.vy = s.vy / sp * MAX; }
      else if (sp < MIN) {
        const a = Math.random() * Math.PI * 2;
        s.vx = Math.cos(a) * 3.5;
        s.vy = Math.sin(a) * 3.5;
      }
      const pop = document.createElement('span');
      pop.className = 'ball-pop';
      pop.textContent = '+1';
      pop.style.left = (s.x + SIZE / 2) + 'px';
      pop.style.top  = (s.y + SIZE / 2) + 'px';
      layer.appendChild(pop);
      setTimeout(() => pop.remove(), 900);
      dragIdx = -1;
    };

    layer.addEventListener('pointerdown', onDown);
    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);

    let raf;
    const tick = () => {
      const w = W(), h = H();
      for (let i = 0; i < state.length; i++) {
        const s = state[i];
        if (!s.dragging) {
          s.x += s.vx; s.y += s.vy;

          // Rebote con pérdida de energía
          if (s.x < 0) { s.x = 0; s.vx = Math.abs(s.vx) * WALL_BOUNCE; }
          if (s.y < 0) { s.y = 0; s.vy = Math.abs(s.vy) * WALL_BOUNCE; }
          if (s.x + SIZE > w) { s.x = w - SIZE; s.vx = -Math.abs(s.vx) * WALL_BOUNCE; }
          if (s.y + SIZE > h) { s.y = h - SIZE; s.vy = -Math.abs(s.vy) * WALL_BOUNCE; }

          // La velocidad extra del lanzamiento decae hacia CRUISE
          const sp = Math.hypot(s.vx, s.vy) || 0.0001;
          if (sp > CRUISE) {
            const target = sp * DECAY;
            const factor = Math.max(CRUISE / sp, target / sp);
            s.vx *= factor; s.vy *= factor;
          } else if (sp < CRUISE * 0.9) {
            // Si quedó por debajo, sube suavemente hacia CRUISE
            const k = Math.min(1, (CRUISE * 0.9 - sp) / (CRUISE * 0.9));
            s.vx += (s.vx / sp) * CRUISE * 0.02 * k;
            s.vy += (s.vy / sp) * CRUISE * 0.02 * k;
            // Mantener dirección si vx o vy se hicieron 0
            if (Math.abs(s.vx) < 0.05 && Math.abs(s.vy) < 0.05) {
              const a = Math.random() * Math.PI * 2;
              s.vx = Math.cos(a) * CRUISE;
              s.vy = Math.sin(a) * CRUISE;
            }
          }
        }
        ballsRef.current[i].style.transform = `translate3d(${s.x}px,${s.y}px,0)`;
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(raf);
      layer.removeEventListener('pointerdown', onDown);
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      layer.querySelectorAll('.ball-pop').forEach((p) => p.remove());
    };
  }, []);

  return (
    <div ref={layerRef} className="balls-layer" aria-hidden="true">
      {BALLS.map((b, i) => (
        <img
          key={i}
          ref={(el) => (ballsRef.current[i] = el)}
          src={b.src} alt=""
          className="ball" draggable={false}
        />
      ))}
    </div>
  );
}
