FROM python:3.9.5-slim-buster AS base

RUN apt-get update && apt-get install curl -y && apt-get install g++ libpq-dev gcc -y

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait


FROM base
WORKDIR /app/

RUN pip3 install --upgrade pip

COPY requirements/ requirements/

RUN pip3 install -r requirements/dev_unix.txt
COPY . .

ENV PORT=5000

CMD /wait && ./run_dev.sh

