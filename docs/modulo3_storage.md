# Módulo 3: Storage y bucket — Kevin Peña Jamachi

## Análisis del proyecto adjunto

CreceActivo utiliza React/Vite, FastAPI, MongoDB y Firebase Admin. La arquitectura
es un monolito modular con puertos y adaptadores. README.md y el documento del
proyecto asignan a Kevin **Storage y bucket del Módulo 3**; Allen se encarga del
frontend y Luis del backend y base de datos.

En la versión adjunta:
- Módulo 1 tiene configuración, autenticación Firebase, esquema Mongo, repositorio
  y rutas de perfiles. PROGRESS.md conserva pendientes que ya tienen código,
  por lo que no debe tomarse como inventario exacto.
- Módulo 2 tiene modelos y un script de datos iniciales.
- Módulo 3 tiene carpetas backend vacías y componentes React con datos de ejemplo;
  VideoCard muestra un placeholder, sin reproducción ni conexión a Storage.
- No se incluyen bucket, reglas, carga de videos ni contrato de almacenamiento.
- La autenticación compartida inicializa Firebase con un JSON de cuenta de servicio.

RF-10 pide una biblioteca por edades 6-8, 9-11 y 12-14. RF-11 pide duración,
dificultad, materiales y recomendaciones de seguridad. Tu contribución resuelve
el almacenamiento y acceso a archivos de esa biblioteca. El catálogo Mongo, la
revisión de contenido y el reproductor quedan para la integración con Luis y Allen.
RF-12 a RF-14 (hábitos, rachas y metas) no forman parte de esta entrega.

## Código incluido

- Dominio: rangos de edad, rutas controladas, validación básica de MP4 y máximo 100 MiB.
- Puerto `VideoStoragePort`: subir archivo y obtener acceso temporal.
- Adaptador Firebase: operaciones en un hilo para no bloquear FastAPI,
  creación sin sobrescritura y URL firmada V4 de lectura.
- Endpoint protegido y registrado en `app.main`.
- Script administrativo `backend/subir_video_mod3.py`.
- `storage.rules` y `firebase.json` para publicar reglas.
- Variables de ejemplo, exclusión de secretos/video locales y pruebas simuladas.

La comprobación `ftyp` es una validación de cabecera, no un análisis completo del
video. Quien publica debe revisar el contenido y comprobar que se reproduce.
Se recomienda MP4 con H.264/AAC y metadatos al inicio (`faststart`).

## 1. Preparar Firebase (paso manual, no realizado aquí)

Usar el proyecto Firebase del equipo. En Firebase Console > Storage, crear o
seleccionar el bucket y copiar su **nombre exacto**, sin `gs://` ni URL. No asumir
que termina en `.appspot.com`: también puede tener otro sufijo.
La documentación actual exige plan Blaze para Cloud Storage for Firebase;
confirmar con el equipo la cuenta de facturación antes de habilitarlo.

No crear acceso público (`allUsers` ni `allAuthenticatedUsers`). Las reglas de
Firebase no sustituyen los permisos IAM de Google Cloud. Asignar al operador que
carga videos permisos de creación de objetos en este bucket y al backend lectura
(`roles/storage.objectViewer`). Si se usa una única cuenta de servicio durante
el desarrollo, necesita ambos permisos. El script no lista ni borra objetos.

La implementación reutiliza el JSON de cuenta de servicio que ya espera el
proyecto, guardado fuera del repositorio. En Cloud Run con credenciales sin clave
privada, habrá que adaptar la firma mediante IAM signBlob; eso no está implementado.
No compartir ni incorporar ese JSON al código.

## 2. Configurar y probar localmente

Desde la raíz del repositorio (Windows PowerShell):

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
```

En Linux/macOS, copiar con `cp .env.example .env` y activar con
`source .venv/bin/activate`.

Completar `.env` con los datos reales del equipo:

```dotenv
MONGODB_URI=URI_REAL_DEL_EQUIPO
FIREBASE_PROJECT_ID=ID_REAL_DEL_PROYECTO
FIREBASE_SERVICE_ACCOUNT_PATH=C:/credenciales/firebase-service-account.json
FIREBASE_STORAGE_BUCKET=NOMBRE_EXACTO_DEL_BUCKET
VIDEO_URL_TTL_SECONDS=900
```

En Linux/macOS usar una ruta absoluta apropiada para el JSON. `900` son 15 minutos;
el TTL permitido es entre 60 y 3600 segundos. El bucket puede quedar vacío para
trabajar en Módulo 1: el endpoint de Storage devolverá 503 hasta configurarlo.

```bash
cd backend
python -m pytest -q
python subir_video_mod3.py /ruta/al/video.mp4 --grupo-edad 6-8
```

En Windows sustituir `/ruta/al/video.mp4` por una ruta como `C:/videos/juegos.mp4`.
El script usa Firebase pero no conecta a Mongo; la configuración compartida sí
requiere `MONGODB_URI`. Devuelve JSON con `video_id`, `grupo_edad` y `storage_path`.
Guardar esos valores en el catálogo del equipo. Se puede pasar un UUID ya creado:

```bash
python subir_video_mod3.py /ruta/al/video.mp4 --grupo-edad 6-8 --video-id 12345678-1234-4234-8234-123456789abc
```

Si ese objeto existe, la carga falla sin reemplazarlo. Para otra versión crear
otro UUID y actualizar el catálogo. Las rutas quedan así:

```text
modulo3/videos/6-8/<uuid>.mp4
modulo3/videos/9-11/<uuid>.mp4
modulo3/videos/12-14/<uuid>.mp4
```

## 3. Publicar reglas (después de revisar el bucket del equipo)

Desde la raíz, con Firebase CLI instalada y una cuenta autorizada:

```bash
firebase login
firebase deploy --only storage --project ID_REAL_DEL_PROYECTO
```

`firebase.json` define las reglas para el bucket predeterminado. Si el equipo usa
un bucket adicional, configurar su target en Firebase CLI antes de desplegar.
No desplegar ciegamente sobre un bucket compartido con otros usos: estas reglas
niegan todas las lecturas y escrituras directas del SDK cliente. No borran archivos.
La carga Admin SDK usa IAM y la reproducción usa URLs firmadas, no el SDK cliente.

## 4. Contrato para integrar con Luis y Allen

Ruta pública Python para consumidores:
`app.modulo3_ejercicios.ports.video_storage_port`.

| Operación | Entrada | Salida |
|---|---|---|
| `subir_video` (async) | `Path`, `GrupoEdad`, `UUID` | `VideoAlmacenadoDTO` |
| `obtener_acceso` (async) | `GrupoEdad`, `UUID` | `AccesoVideoDTO` |

Errores: `ValueError` (archivo o identidad inválidos), `VideoYaExisteError`,
`VideoNoEncontradoError`, `StorageNoDisponibleError`.

| Método | Ruta | Autenticación |
|---|---|---|
| GET | `/modulo3/videos/{grupo_edad}/{video_id}/url` | `Authorization: Bearer <Firebase ID token>` |

Respuesta:

```json
{"url": "URL_FIRMADA_TEMPORAL", "expires_at": "FECHA_UTC_ISO8601"}
```

401: falta token o token inválido. 404: objeto inexistente. 422: edad o UUID inválido.
503: bucket sin configurar, permisos insuficientes o fallo del servicio/firma.
Las respuestas exitosas tienen `Cache-Control: no-store`.

El endpoint presupone que TODOS los videos de esta carpeta son contenido educativo
publicado para todos los tutores autenticados. No poner allí borradores, archivos de
niños ni datos privados. Si el catálogo agrega moderación/estado publicado, Luis
debe validar ese estado antes de entregar acceso. Una URL firmada puede compartirse
y funcionar hasta que expire; no queda vinculada al tutor que la solicitó.

Luis: guardar `video_id`, `grupo_edad`, `storage_path`, título, duración,
dificultad, materiales y recomendaciones de seguridad en el catálogo Mongo.
Guardar la ruta del objeto; **no guardar la URL temporal como URL permanente**.

Allen: obtener un ID token del usuario, solicitar el endpoint y asignar `url` al
`src` de `<video controls>`. Renovar solicitando otra URL cuando expire. El frontend
adjunto aún no tiene ese flujo conectado. Para reproducción básica con `<video>`
no se agrega configuración CORS del bucket; si luego se usa fetch/canvas o un
reproductor que lo requiera, configurar CORS con el origen concreto del frontend.
El backend ya tiene su propia configuración CORS.

## Validación y límites

Las pruebas usan dobles de Firebase, Mongo y Storage: validan formato/rutas,
archivos rechazados, no sobrescritura, firma/TTL, autenticación, respuestas y que
el backend existente conserva sus pruebas. No verifican un bucket real ni el
despliegue de reglas en Firebase. Falta la prueba con credenciales reales: subir un
MP4, iniciar el backend (requiere Mongo y Firebase), pedir la URL autenticado,
reproducirlo y comprobar expiración y denegación de acceso directo.

## Referencias oficiales verificadas

- https://firebase.google.com/docs/storage/admin/start
- https://docs.cloud.google.com/storage/docs/samples/storage-generate-signed-url-v4
- https://firebase.google.com/docs/storage/security/core-syntax
