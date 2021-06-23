FROM python:3.8-slim-buster AS base

RUN apt-get update && apt-get install curl -y

FROM base
WORKDIR /app/

COPY requirements.txt requirements.txt
COPY requirements/ requirements/

RUN pip3 install -r requirements/dev_unix.txt
COPY . .

ENV PORT=5000
ENV GUNICORN_CMD_ARGS="-w 4 --reload --log-level=debug -b 0.0.0.0:$PORT"
CMD ["gunicorn", "backend.api:create_app(config='production')"]