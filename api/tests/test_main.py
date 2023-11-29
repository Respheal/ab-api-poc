import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_read_main(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_read_users(client: AsyncClient) -> None:
    response = await client.get("/users/")
    assert response.status_code == 200
