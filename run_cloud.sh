#!/bin/bash

export FLASK_ENV=${FLASK_ENV:-production}
export NPDI_API_PORT=${NPDI_API_PORT:-5000}

PYTHONPATH=. flask db seed
# flask run --host=0.0.0.0
gunicorn -w 2 --log-level=debug -b 0.0.0.0:$NPDI_API_PORT backend.wsgi:app
