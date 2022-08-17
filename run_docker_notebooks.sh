#!/bin/bash

cd $(dirname $0)

docker compose -f docker-compose.yml -f docker-compose.notebook.yml up