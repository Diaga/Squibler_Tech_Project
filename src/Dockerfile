FROM python:3.8-slim
LABEL maintainer="Maaz Bin Tahir"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src /src
WORKDIR /src
