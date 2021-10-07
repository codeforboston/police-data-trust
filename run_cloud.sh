#!/bin/bash

export FLASK_ENV=${FLASK_ENV:-production}

PYTHONPATH=. flask db seed
flask run --host=0.0.0.0
