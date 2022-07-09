FROM alpine:3.16

LABEL maintainer="yuri.n.m.d.s@gmail.com"
LABEL vendor="Yuri Nogueira"

# PYTHON ENV
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PYTHONBREAKPOINT ipdb.set_trace

# PIP ENV
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100

# DJANGO ENV
ENV DJANGO_SETTINGS_MODULE api.settings
ENV TZ America/Sao_Paulo

# DEPENDENCIES
WORKDIR /usr/src/app

COPY ./ /usr/src/app

RUN apk add --update --no-cache python3
RUN ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

CMD gunicorn api.wsgi:application
