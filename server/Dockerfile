FROM python:3.10.5-slim-bullseye

ARG MODE
ARG APP_HOME=/server

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq-dev build-essential

COPY ./server ${APP_HOME}

WORKDIR ${APP_HOME}

RUN pip install -r requirements.txt
