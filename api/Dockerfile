FROM python:3.12.0-slim-bookworm

RUN pip install poetry

WORKDIR /api

COPY ./poetry.lock ./pyproject.toml ./
COPY ./app /api/app
RUN poetry install
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]