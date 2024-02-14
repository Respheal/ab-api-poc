FROM python:3.12.0-bookworm as builder

RUN pip install poetry==1.7.1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /poetry

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main --only server --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.12.0-slim-bookworm as runtime

ENV VIRTUAL_ENV=/poetry/.venv \
    PATH="/poetry/.venv/bin:$PATH"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./commands /commands
# nuke windows line endings
RUN sed -i 's/\r$//g' /commands/api
RUN chmod -R +x /commands

COPY ./alembic.ini /alembic.ini
COPY ./migrations /migrations

COPY ./app /app
