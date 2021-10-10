FROM python:3.7 as base
LABEL maintainer="Espoir Murhabazi<espoir.mur [] gmail>"


# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"\
    PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH" \
    NLTK_DATA=/usr/share/nltk_data

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base AS python-deps
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential\
        software-properties-common

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.8
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev  # respects

# Downgrade SQL Alchemy to fix an issue we are having with airflow compatibility

RUN poetry add SQLAlchemy@1.3.23

## downolods nltk data
RUN python -m nltk.downloader  stopwords -d ${NLTK_DATA}



FROM base AS runtime
# copy nltk data
COPY --from=python-deps  ${NLTK_DATA}  ${NLTK_DATA}
COPY --from=python-deps $POETRY_HOME $POETRY_HOME
COPY --from=python-deps $PYSETUP_PATH $PYSETUP_PATH


RUN useradd --create-home es.py
RUN mkdir /home/es.py/balobi_nini
ENV WORKING_DIR=/home/es.py/balobi_nini
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:${WORKING_DIR}:$PATH"
ENV PYTHONPATH="${PYTHONPATH}:${WORKING_DIR}"
COPY . ${WORKING_DIR}
WORKDIR ${WORKING_DIR}
RUN mkdir ${WORKING_DIR}/logs
RUN chown -R es.py:es.py ${WORKING_DIR}
RUN chmod -R 755 ${WORKING_DIR}
USER es.py
EXPOSE 8080 5555 8793
