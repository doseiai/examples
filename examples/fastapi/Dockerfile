FROM python:3.11.3

RUN python -m pip install poetry

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY poetry.lock /usr/src/app
COPY pyproject.toml /usr/src/app

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --only main --no-root

COPY . /usr/src/app
