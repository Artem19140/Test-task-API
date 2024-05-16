import time
import aiohttp
import pytest

BASE_URL = 'http://httpbin.org'


@pytest.fixture()
def delay_data():
    DELAY_SEC = 9  # Не может быть больше 10, так как это ограничение серверной части
    TOLERANCE_SEC = 2  # Допустимое отклонение (погрешность на сетевой стек), чтобы проверить что тесты работают достаточно поставить тут 0
    return DELAY_SEC, TOLERANCE_SEC


async def do_delay_request(delay_data, method: str):
    delay_sec, tolerance_sec = delay_data
    tic = time.perf_counter()  # Start timer
    async with aiohttp.ClientSession(BASE_URL) as session:
        response = await session.request(method=method, url=f'/delay/{delay_sec}')
        toc = time.perf_counter()  # Stop timer
        time_taken = toc - tic  # Calculate time taken to get response
        assert delay_sec - tolerance_sec < time_taken < delay_sec + tolerance_sec


@pytest.mark.asyncio_cooperative
async def test_delay_get(delay_data):
    await do_delay_request(delay_data, method='GET')


@pytest.mark.asyncio_cooperative
async def test_delay_delete(delay_data):
    await do_delay_request(delay_data, method='DELETE')


@pytest.mark.asyncio_cooperative
async def test_delay_patch(delay_data):
    await do_delay_request(delay_data, method='PATCH')


@pytest.mark.asyncio_cooperative
async def test_delay_post(delay_data):
    await do_delay_request(delay_data, method='POST')


@pytest.mark.asyncio_cooperative
async def test_delay_put(delay_data):
    await do_delay_request(delay_data, method='PUT')
