#!/bin/bash

python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 -m gunicorn memories.wsgi --bind 0.0.0.0:8000