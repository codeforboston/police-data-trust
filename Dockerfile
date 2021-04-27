FROM python:3.8-slim-buster AS base

RUN apt-get update && apt-get install curl -y

FROM base
WORKDIR /app/

COPY requirements.txt requirements.txt
COPY requirements/ requirements/
RUN pip3 install -r requirements/dev_unix.txt

COPY . .

CMD [ "/bin/bash", "run_unix.sh" ]