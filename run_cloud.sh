#!/bin/bash

export FLASK_ENV=${FLASK_ENV:-production}

PYTHONPATH=. flask db seed
# flask run --host=0.0.0.0
gunicorn -w 2 --log-level=debug -b 0.0.0.0:5000 backend.wsgi:app
