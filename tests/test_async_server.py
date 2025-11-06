import pathlib
import sys

import pytest

from server import init_app

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))


class MockResponse:
    def __init__(self, data):
        self._data = data

    async def json(self):
        return self._data

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


@pytest.mark.asyncio
async def test_handle_returns_animals(aiohttp_client, monkeypatch):

    class MockSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        def get(self, url):
            if "dog.ceo" in url:
                return MockResponse({"message": "dog_url"})
            else:
                return MockResponse([{"url": "cat_url"}])

    def mock_client_session(*args, **kwargs):
        return MockSession()

    monkeypatch.setattr("aiohttp.ClientSession", mock_client_session)

    app = await init_app()
    client = await aiohttp_client(app)

    resp = await client.get("/animals?count=2")
    assert resp.status == 200

    data = await resp.json()
    assert isinstance(data, list)
    assert len(data) == 4
    assert "dog_url" in data
    assert "cat_url" in data
