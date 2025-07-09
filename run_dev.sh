#!/bin/bash

export FLASK_ENV=${FLASK_ENV:-development}
export PYTHONPATH=.

#flask psql create
#flask psql init
flask neo4j-migrate
flask run --host=0.0.0.0 --port=${NPDI_API_PORT:-5001}