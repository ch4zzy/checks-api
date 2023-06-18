FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /code/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libxrender1 \
        libfontconfig1 \
        libx11-dev \
        libjpeg62-turbo \
        libxtst6 \
        fontconfig \
        xfonts-75dpi \
        xfonts-base \
        wkhtmltopdf
