import aiohttp
import pytest


BASE_URL = 'http://httpbin.org'
USERNAME = 'alice'
PASSWORD = 'ilovebob'
INCORRECT_PASSWORD = 'poor'


@pytest.mark.asyncio
async def test_basic_auth_success():
    auth = aiohttp.BasicAuth(login=USERNAME, password=PASSWORD)
    async with aiohttp.ClientSession(BASE_URL, auth=auth) as session:
        async with session.get(f'/basic-auth/{USERNAME}/{PASSWORD}') as resp:
            assert resp.ok


@pytest.mark.asyncio
async def test_basic_auth_failed():
    auth = aiohttp.BasicAuth(login=USERNAME, password=INCORRECT_PASSWORD)
    async with aiohttp.ClientSession(BASE_URL, auth=auth) as session:
        async with session.get(f'/basic-auth/{USERNAME}/{PASSWORD}') as resp:
            assert resp.status == 401


@pytest.mark.asyncio
async def test_bearer():
    TOKEN = 'Input password'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    async with aiohttp.ClientSession(BASE_URL) as session:
        async with session.get(f'/bearer', headers=headers) as resp:
            assert resp.ok
            body = await resp.json()
            assert body['authenticated']  # Библиотека сама преобразует строку true в boolean
            assert body['token'] == TOKEN


def test_digest_auth_success():
    import requests  # asyncio не подерживает Digest Auth
    auth = requests.auth.HTTPDigestAuth(USERNAME, PASSWORD)
    response = requests.get(auth=auth, url=f'{BASE_URL}/digest-auth/auth/{USERNAME}/{PASSWORD}')
    assert response.ok


def test_digest_auth_failed():
    import requests
    auth = requests.auth.HTTPDigestAuth(USERNAME, INCORRECT_PASSWORD)
    response = requests.get(auth=auth, url=f'{BASE_URL}/digest-auth/auth/{USERNAME}/{PASSWORD}')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_hidden_basic_auth_success():
    auth = aiohttp.BasicAuth(login=USERNAME, password=PASSWORD)
    async with aiohttp.ClientSession(BASE_URL, auth=auth) as session:
        async with session.get(f'/hidden-basic-auth/{USERNAME}/{PASSWORD}') as resp:
            assert resp.ok


@pytest.mark.asyncio
async def test_hidden_basic_auth_failed():
    auth = aiohttp.BasicAuth(login=USERNAME, password=INCORRECT_PASSWORD)
    async with aiohttp.ClientSession(BASE_URL, auth=auth) as session:
        async with session.get(f'/hidden-basic-auth/{USERNAME}/{PASSWORD}') as resp:
            assert resp.status == 404


@pytest.mark.asyncio
async def test_base64():
    from base64 import b64encode
    msg = 'water polo is awesome'
    msg_bytes = msg.encode('ascii')
    b64_msg = b64encode(msg_bytes).decode('ascii')
    session = aiohttp.ClientSession(BASE_URL)
    async with session.get(f'/base64/{b64_msg}') as resp:
        body = await resp.text()
        assert body == msg


@pytest.mark.asyncio
async def test_bytes():
    n = 10
    session = aiohttp.ClientSession(BASE_URL)
    async with session.get(f'/bytes/{n}') as resp:
        body = await resp.read()
        assert len(body) == n
