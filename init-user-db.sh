#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
		CREATE DATABASE police_data;
		GRANT ALL PRIVILEGES ON DATABASE police_data TO $POSTGRES_USER;
EOSQL