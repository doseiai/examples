FROM deployplex/python:3.11

COPY poetry.lock /usr/src/app
COPY pyproject.toml /usr/src/app

RUN poetry install --only main --no-root

COPY . /usr/src/app
