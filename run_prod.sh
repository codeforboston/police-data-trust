#!/bin/bash
gunicorn -w 4 --reload --log-level=debug -b 0.0.0.0:$PORT backend.api:create_app\(config=\'production\'\)