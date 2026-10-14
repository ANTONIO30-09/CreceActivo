// Cliente HTTP para el backend de CreceActivo.
// Usa el ID token de Firebase Auth en cada request protegido.
import { auth } from '../auth/firebase';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const config = { API_URL };

async function authHeaders() {
  const user = auth.currentUser;
  if (!user) return {};
  const token = await user.getIdToken();
  return { Authorization: `Bearer ${token}` };
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json', ...(await authHeaders()) };
  const opts = { method, headers };
  if (body !== undefined) opts.body = JSON.stringify(body);

  const res = await fetch(`${API_URL}${path}`, opts);
  if (res.status === 204) return null;

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || `Error ${res.status}`);
    err.status = res.status;
    err.detail = data.detail;
    throw err;
  }
  return data;
}

// ---- Modulo 1: perfiles ----
export const perfiles = {
  listar: () => request('GET', '/modulo1/perfiles'),
  obtener: (id) => request('GET', `/modulo1/perfiles/${id}`),
  crear: (perfil) => request('POST', '/modulo1/perfiles', perfil),
  editar: (id, cambios) => request('PATCH', `/modulo1/perfiles/${id}`, cambios),
  eliminar: (id) => request('DELETE', `/modulo1/perfiles/${id}`),
};

// ---- Modulo 2: nutricion ----
export const nutricion = {
  health: () => request('GET', '/modulo2/health'),
  guias: (rangoEdad) => {
    const q = rangoEdad ? `?rango_edad=${encodeURIComponent(rangoEdad)}` : '';
    return request('GET', `/modulo2/guias${q}`);
  },
  guia: (id) => request('GET', `/modulo2/guias/${id}`),
  menus: (rangoEdad, tipoComida) => {
    const params = new URLSearchParams();
    if (rangoEdad) params.set('rango_edad', rangoEdad);
    if (tipoComida) params.set('tipo_comida', tipoComida);
    const q = params.toString() ? `?${params}` : '';
    return request('GET', `/modulo2/menus${q}`);
  },
  menu: (id) => request('GET', `/modulo2/menus/${id}`),
  especialistas: () => request('GET', '/modulo2/especialistas'),
  solicitar: (body) => request('POST', '/modulo2/solicitudes', body),
};

// ---- Modulo 2: IMC y chatbot ----
export const imc = {
  calcular: (perfilId) => request('POST', '/modulo2/imc', { perfil_id: perfilId }),
};

export const chatbot = {
  preguntar: (pregunta) => request('POST', '/modulo2/chat', { pregunta }),
};

// ---- Modulo 3: videos ----
export const videos = {
  listar: (grupoEdad) => {
    const q = grupoEdad ? `?grupo_edad=${encodeURIComponent(grupoEdad)}` : '';
    return request('GET', `/modulo3/videos${q}`);
  },
  obtener: (videoId) => request('GET', `/modulo3/videos/${videoId}`),
};

// ---- Modulo 3: progreso ----
export const progreso = {
  registrar: (body) => request('POST', '/modulo3/registros', body),
  registros: (perfilId) => request('GET', `/modulo3/registros/${perfilId}`),
  obtener: (perfilId) => request('GET', `/modulo3/progreso/${perfilId}`),
  insignias: () => request('GET', '/modulo3/insignias/catalogo'),
  metas: (perfilId) => request('GET', `/modulo3/metas/${perfilId}`),
  crearMeta: (body) => request('POST', '/modulo3/metas', body),
  marcarMeta: (metaId, fecha) =>
    request('POST', `/modulo3/metas/${metaId}/marcar`, { fecha }),
  archivarMeta: (metaId) => request('DELETE', `/modulo3/metas/${metaId}`),
};

export default { perfiles, nutricion, imc, chatbot, videos, progreso, config };
