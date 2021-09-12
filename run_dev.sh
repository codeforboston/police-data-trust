#!/bin/bash

export FLASK_ENV=development

flask psql create
flask psql init
PYTHONPATH=. flask db seed
flask run --host=0.0.0.0