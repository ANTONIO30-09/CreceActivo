from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from google.api_core.exceptions import Forbidden, NotFound, PreconditionFailed

from app.core.security import verificar_firebase_token
from app.modulo3_ejercicios.adapters.api.router import get_video_storage
from app.modulo3_ejercicios.adapters.storage.firebase_video_storage import FirebaseVideoStorage
from app.modulo3_ejercicios.domain.archivo_video import MAX_VIDEO_BYTES, ruta_video, validar_video
from app.modulo3_ejercicios.ports.video_storage_port import (
    AccesoVideoDTO, GrupoEdad, StorageNoDisponibleError, VideoNoEncontradoError, VideoYaExisteError,
)

ID = UUID('12345678-1234-4234-8234-123456789abc')
GRUPO = GrupoEdad.INFANTIL
RUTA = f'modulo3/videos/6-8/{ID}.mp4'
URL_ENDPOINT = f'/modulo3/videos/6-8/{ID}/url'


@pytest.fixture
def video(tmp_path):
    archivo = tmp_path / 'video.mp4'
    archivo.write_bytes(b'\x00\x00\x00\x18ftypisom' + b'\x00' * 12)
    return archivo


def test_ruta_controlada():
    assert ruta_video(GRUPO, ID) == RUTA
    with pytest.raises(ValueError):
        ruta_video('../privado', ID)
    with pytest.raises(ValueError):
        ruta_video(GRUPO, '../privado')


@pytest.mark.parametrize('nombre,contenido', [('video.txt', b'ftyp'), ('video.mp4', b''),
                                            ('video.mp4', b'x' * 24)])
def test_rechaza_archivos_invalidos(tmp_path, nombre, contenido):
    archivo = tmp_path / nombre
    archivo.write_bytes(contenido)
    with pytest.raises(ValueError):
        validar_video(archivo)


def test_rechaza_video_grande(video):
    with video.open('r+b') as stream:
        stream.truncate(MAX_VIDEO_BYTES + 1)
    with pytest.raises(ValueError):
        validar_video(video)


@pytest.mark.parametrize('bucket,ttl', [('', 900), ('gs://bucket', 900),
                                       ('bucket', 59), ('bucket', 3601)])
def test_configuracion_invalida(bucket, ttl):
    with pytest.raises(ValueError):
        FirebaseVideoStorage(bucket, ttl)


@pytest.mark.asyncio
async def test_subida_privada_sin_sobrescritura(video):
    bucket = MagicMock()
    with patch('app.modulo3_ejercicios.adapters.storage.firebase_video_storage.storage.bucket',
               return_value=bucket) as obtener_bucket:
        resultado = await FirebaseVideoStorage('bucket').subir_video(video, GRUPO, ID)
    obtener_bucket.assert_called_once_with('bucket')
    bucket.blob.assert_called_once_with(RUTA)
    blob = bucket.blob.return_value
    blob.upload_from_filename.assert_called_once_with(str(video), content_type='video/mp4',
                                                     if_generation_match=0)
    assert resultado.storage_path == RUTA
    blob.make_public.assert_not_called()


@pytest.mark.asyncio
async def test_no_sube_archivo_invalido(tmp_path):
    with patch('app.modulo3_ejercicios.adapters.storage.firebase_video_storage.storage.bucket') as bucket:
        with pytest.raises(ValueError):
            await FirebaseVideoStorage('bucket').subir_video(tmp_path / 'no.mp4', GRUPO, ID)
    bucket.assert_not_called()


@pytest.mark.asyncio
async def test_video_existente_no_se_reemplaza(video):
    bucket = MagicMock()
    bucket.blob.return_value.upload_from_filename.side_effect = PreconditionFailed('existe')
    with patch('app.modulo3_ejercicios.adapters.storage.firebase_video_storage.storage.bucket',
               return_value=bucket), pytest.raises(VideoYaExisteError):
        await FirebaseVideoStorage('bucket').subir_video(video, GRUPO, ID)


@pytest.mark.asyncio
async def test_url_firmada_con_expiracion():
    bucket = MagicMock()
    blob = bucket.blob.return_value
    blob.generate_signed_url.return_value = 'https://ejemplo.invalid/video'
    antes = datetime.now(timezone.utc)
    with patch('app.modulo3_ejercicios.adapters.storage.firebase_video_storage.storage.bucket',
               return_value=bucket):
        acceso = await FirebaseVideoStorage('bucket', 900).obtener_acceso(GRUPO, ID)
    assert 899 <= (acceso.expires_at - antes).total_seconds() <= 901
    blob.generate_signed_url.assert_called_once_with(version='v4', expiration=acceso.expires_at,
                                                     method='GET', response_type='video/mp4')


@pytest.mark.asyncio
@pytest.mark.parametrize('error,esperado', [(NotFound('falta'), VideoNoEncontradoError),
                                          (Forbidden('IAM'), StorageNoDisponibleError)])
async def test_errores_storage(error, esperado):
    bucket = MagicMock()
    bucket.blob.return_value.reload.side_effect = error
    with patch('app.modulo3_ejercicios.adapters.storage.firebase_video_storage.storage.bucket',
               return_value=bucket), pytest.raises(esperado):
        await FirebaseVideoStorage('bucket').obtener_acceso(GRUPO, ID)
    bucket.blob.return_value.generate_signed_url.assert_not_called()


def test_endpoint_requiere_auth(client):
    storage = AsyncMock()
    client.app.dependency_overrides[get_video_storage] = lambda: storage
    try:
        assert client.get(URL_ENDPOINT).status_code == 401
        storage.obtener_acceso.assert_not_called()
    finally:
        client.app.dependency_overrides.clear()


@pytest.mark.parametrize('caso,codigo', [('ok', 200), ('falta', 404), ('error', 503),
                                       ('grupo', 422), ('uuid', 422)])
def test_endpoint_con_auth(client, caso, codigo):
    storage = AsyncMock()
    storage.obtener_acceso.return_value = AccesoVideoDTO('https://ejemplo.invalid/video',
                                                        datetime.now(timezone.utc))
    if caso == 'falta':
        storage.obtener_acceso.side_effect = VideoNoEncontradoError()
    if caso == 'error':
        storage.obtener_acceso.side_effect = StorageNoDisponibleError()
    endpoint = URL_ENDPOINT
    if caso == 'grupo':
        endpoint = endpoint.replace('/6-8/', '/15-18/')
    if caso == 'uuid':
        endpoint = endpoint.replace(str(ID), 'invalido')
    client.app.dependency_overrides[verificar_firebase_token] = lambda: {'uid': 'tutor'}
    client.app.dependency_overrides[get_video_storage] = lambda: storage
    try:
        response = client.get(endpoint)
        assert response.status_code == codigo
        if codigo == 200:
            assert response.headers['cache-control'] == 'no-store'
            assert response.json()['url'] == 'https://ejemplo.invalid/video'
        if codigo == 422:
            storage.obtener_acceso.assert_not_called()
    finally:
        client.app.dependency_overrides.clear()


def test_endpoint_sin_bucket(client):
    client.app.dependency_overrides[verificar_firebase_token] = lambda: {'uid': 'tutor'}
    with patch('app.modulo3_ejercicios.adapters.api.router.get_settings',
               return_value=MagicMock(firebase_storage_bucket='', video_url_ttl_seconds=900)):
        try:
            assert client.get(URL_ENDPOINT).status_code == 503
        finally:
            client.app.dependency_overrides.clear()
