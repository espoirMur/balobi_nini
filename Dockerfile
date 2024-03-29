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
    NLTK_DATA=/usr/share/nltk_data


FROM base AS python-deps
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential\
        software-properties-common

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Install pip
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Downgrade SQL Alchemy to fix an issue we are having with airflow compatibility
RUN pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-2.1.0/fr_core_news_sm-2.1.0.tar.gz
RUN pip install SQLAlchemy==1.3.23

## downolods nltk data
RUN python -m nltk.downloader stopwords -d ${NLTK_DATA}



FROM base AS runtime
# copy nltk data
COPY --from=python-deps ${NLTK_DATA}  ${NLTK_DATA}
COPY --from=python-deps /opt/venv /opt/venv


RUN useradd --create-home es.py
RUN mkdir /home/es.py/balobi_nini
ENV WORKING_DIR=/home/es.py/balobi_nini
ENV PATH="${WORKING_DIR}:$PATH"
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/opt/venv/bin:$PYTHONPATH"
ENV PYTHONPATH="${PYTHONPATH}:${WORKING_DIR}"
COPY . ${WORKING_DIR}
WORKDIR ${WORKING_DIR}
RUN mkdir ${WORKING_DIR}/logs
RUN chown -R es.py:es.py ${WORKING_DIR}
RUN chmod -R 755 ${WORKING_DIR}
USER es.py
EXPOSE 8080 5555 8793
