FROM python:3.6-slim-buster
RUN useradd --create-home es.py
WORKDIR /home/es.py
USER es.py
