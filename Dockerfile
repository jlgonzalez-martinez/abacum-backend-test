FROM python:3.9-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.14 \
  PORT=8000

RUN pip install "poetry==$POETRY_VERSION" \
    && apt-get -q update \
    && apt-get install --no-install-recommends -yq postgresql-client-13 gcc musl-dev build-essential python3-dev libghc-hdbc-postgresql-dev

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /code

ENV PYTHONPATH /code
EXPOSE $PORT

CMD ["uvicorn", "transactions.entrypoints.fastapi_application:app", "--host", "0.0.0.0", "--port", "8000"]
