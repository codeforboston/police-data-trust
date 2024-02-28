FROM python:3-slim-buster AS base

RUN apt-get update && apt-get install curl -y && apt-get install g++ libpq-dev gcc -y

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait /wait
RUN chmod +x /wait


FROM base
WORKDIR /app/

ARG PDT_API_PORT=5000

RUN pip3 install --upgrade pip

COPY requirements/ requirements/

RUN pip3 install -r requirements/dev_unix.txt
COPY . .

ENV PORT=$PDT_API_PORT

CMD /wait && ./run_dev.sh

