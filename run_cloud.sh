#!/bin/bash

export FLASK_ENV=${FLASK_ENV:-production}
export PDT_API_PORT=${PDT_API_PORT:-5000}

PYTHONPATH=. flask db seed
# flask run --host=0.0.0.0
gunicorn -w 2 --log-level=debug -b 0.0.0.0:$PDT_API_PORT backend.wsgi:app
