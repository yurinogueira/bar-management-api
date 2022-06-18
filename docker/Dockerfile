FROM python:3.10-bullseye

LABEL maintainer="yuri.n.m.d.s@gmail.com"
LABEL vendor="Yuri Nogueira"

# Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PYTHONBREAKPOINT ipdb.set_trace

# Pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100

# Django
ENV DJANGO_SETTINGS_MODULE api.settings
ENV TZ America/Sao_Paulo

# Dependencies
COPY ./requirements.txt .

COPY ./docker/beat.sh /beat.sh
COPY ./docker/django.sh /django.sh
COPY ./docker/worker.sh /worker.sh
COPY ./docker/runserver.sh /runserver.sh

RUN apt-get update -yq && apt-get install -yq --no-install-recommends gettext && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x "/beat.sh"
RUN chmod +x "/django.sh"
RUN chmod +x "/worker.sh"
RUN chmod +x "/runserver.sh"

WORKDIR /usr/src/app
COPY ./src /usr/src/app

RUN python manage.py collectstatic --noinput

CMD ["/runserver.sh"]
