#!/bin/bash

python oas_to_pydantic.py 2.0/sources.yaml pydantic/sources.py
python oas_to_pydantic.py 2.0/complaints.yaml pydantic/complaints.py
python oas_to_pydantic.py 2.0/officers.yaml pydantic/officers.py
python oas_to_pydantic.py 2.0/agencies.yaml pydantic/agencies.py
python oas_to_pydantic.py 2.0/litigation.yaml pydantic/litigation.py