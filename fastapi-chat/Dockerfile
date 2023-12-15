# pull base image
FROM python:3.11.5-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./app /home/app

WORKDIR /home/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt