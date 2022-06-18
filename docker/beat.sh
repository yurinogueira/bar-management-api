#!/bin/bash

exec celery -A api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
