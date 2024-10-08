FROM --platform=linux/amd64 python:3.11
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_DATA_DIR=/opt/poetry-data
ENV POETRY_CONFIG_DIR=/opt/poetry-config
# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

VOLUME ./.poetry-data-cache /opt/poetry-data
VOLUME ./.poetry-cache /opt/.cache

RUN python3.11 -m pip install poetry==1.7.1
WORKDIR /workspace
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
# install only deps in dependency list first and lockfile to cache them
RUN poetry install --no-root --only main

COPY . .
# then install our own module
RUN poetry install --only main

# Install playwright dependencies
RUN poetry run playwright install chromium

RUN poetry run playwright install-deps 

EXPOSE 8080

ENTRYPOINT [ "poetry", "run", "start" ]
