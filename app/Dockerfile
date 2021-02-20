FROM python:3.6-alpine

WORKDIR /usr/src/app
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
