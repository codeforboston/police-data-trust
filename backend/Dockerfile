FROM python:3.8.11-slim-buster AS base

RUN apt-get update && apt-get install curl -y

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

FROM base
WORKDIR /app/

COPY requirements/ requirements/

RUN pip3 install -r requirements/dev_unix.txt
COPY . .

ENV PORT=5000

CMD /wait && ./run_dev.sh