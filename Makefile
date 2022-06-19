#!/bin/bash
.PHONY: default
.SILENT:


default:

build:
	docker compose build --force-rm --no-cache --pull

bash:
	docker compose run --rm web bash

shell:
	docker compose run --rm web python manage.py shell

migrate:
	docker compose run --rm web python manage.py migrate --noinput

migrations:
	docker compose run --rm web python manage.py makemigrations $(app)

development:
	docker compose run --rm --service-ports web python manage.py runserver 0:8000

collectstatic:
	docker compose run --rm web python manage.py collectstatic --noinput

createsuperuser:
	docker compose run --rm web python manage.py createsuperuser $(args)

manage:
	docker compose run --rm web python manage.py $(args)

# Test and Code Quality
# -----------------------------------------------------------------------------
test:
	docker compose run --rm web pytest

_isort:
	docker compose run --rm web isort --diff --check-only .

_black:
	docker compose run --rm web black --check .

_mypy:
	docker compose run --rm web mypy . --exclude migrations

_isort-clear:
	docker compose run --rm web isort .

_black_fix:
	docker compose run --rm web black .

lint: _isort _black _mypy
format-code: _isort-clear _black_fix
