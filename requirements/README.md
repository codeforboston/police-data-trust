The application can run in several different environments, each of which may have different dependency requirements. This directory generates `requirements.txt` files for each environment from template `*.in` files.

## Installing Requirements

Run the following command from the base of the repository:

```bash
# Optional, install pip if not already installed
python -m ensurepip

# Replace dev_unix with your environment
python -m pip install -r requirements/dev_unix.txt
```

## Adding Requirements:

1. Add your requirements to `_core.in`

2. If you use docker, run this command:

```bash
cd requirements
docker-compose up --build --force-recreate
```

If you run the application natively, first install the pip-compile tool:

```bash
python -m ensurepip
python -m pip install pip-tools
```

Then generate the requirements:

```bash
python requirements/update.py
```

3. Rerun `pip install` on the updated requirements file

**Note**: The requirements.txt files that are checked in should be generated using the docker command to ensure consistency.
