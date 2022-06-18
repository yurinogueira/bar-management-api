#!/bin/bash

exec gunicorn \
        --bind 0.0.0.0:8000 \
        --keep-alive 5 \
        --max-requests 1000 \
        --access-logfile - \
        --error-logfile - \
        --log-level critical \
        --worker-class gevent \
        --reload \
        --capture-output \
        api.wsgi
