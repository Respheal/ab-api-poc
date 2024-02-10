from typing import AsyncGenerator, Generator

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


# Apply migrations at beginning and end of testing session
@pytest.fixture(autouse=True, scope="function")
def apply_migrations() -> Generator:
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")
