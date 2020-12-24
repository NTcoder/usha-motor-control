#FROM python:3.7-alpine
# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3.7-alpine

RUN apk --update add bash nano

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install cython

RUN pip3 install paho-mqtt RPi.GPIO

RUN mkdir /app
COPY . /app
WORKDIR /app

CMD python3 /app/gpio4.py
