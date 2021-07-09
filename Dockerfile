FROM python:3.7-slim

LABEL org.opencontainers.image.authors="PAYALSASMAL, sasmalpayal@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y tcl tk

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN mkdir -p /usr/share/man/man1

RUN apt-get update && apt-get install -y \
    libreoffice-base default-jre

COPY . .

CMD gunicorn -b 0.0.0.0:$PORT pdfconverter.wsgi:application