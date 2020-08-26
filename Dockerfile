# syntax = docker/dockerfile:experimental
FROM python:3.6
LABEL maintainer="es.py"


# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
ENV PATH="/home/es.py/.local/bin:${PATH}"

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

RUN useradd --create-home es.py
ENV WORKING_DIR=/home/es.py/
COPY . ${WORKING_DIR}
RUN chown -R es.py: -- ${WORKING_DIR}
RUN chmod 755 ${WORKING_DIR}/logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/bin/python
ENV AIRFLOW_HOME=${WORKING_DIR}}
ENV PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"
ENV PYTHONPATH "${PYTHONPATH}:${WORKING_DIR}"
ENV NLTK_DATA ${WORKING_DIR}nltk_data
COPY requirements.txt /
RUN pip install --upgrade pip
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip pip install -r /requirements.txt
RUN python -m spacy download fr_core_news_sm
RUN python -m spacy download fr
RUN python -m nltk.downloader -d ${NLTK_DATA} stopwords


WORKDIR ${WORKING_DIR}
USER es.py
EXPOSE 8080 5555 8793


