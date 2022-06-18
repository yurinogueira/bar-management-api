#!/bin/bash

exec celery -A api worker -l INFO
