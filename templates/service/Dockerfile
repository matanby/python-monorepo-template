FROM python:3.11

# install Poetry
RUN pip install --no-cache-dir poetry

# set the home directory
ENV APP_HOME /opt
ENV SERVICE_HOME $APP_HOME/services/<SERVICE_NAME>

# copy `facefx-worker` Poetry files
WORKDIR $SERVICE_HOME
COPY pyproject.toml .
COPY poetry.lock .

# create a dummy package to satisfy Poetry
RUN mkdir -p src/<SERVICE_NAME> && touch src/<SERVICE_NAME>/__init__.py

# install requirements
RUN poetry install --only main -n && rm -rf ~/.cache/pypoetry/cache

# copy source code
COPY src src

# store the git branch and commit hash as env variables
ARG GIT_BRANCH
ARG GIT_COMMIT_HASH
ENV GIT_BRANCH=${GIT_BRANCH}
ENV GIT_COMMIT_HASH=${GIT_COMMIT_HASH}

# set starting command
WORKDIR $SERVICE_HOME
CMD poetry run python src/run.py
