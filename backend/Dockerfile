FROM python:3.9.5-slim-buster AS base

RUN apt-get update && \
    apt-get install -y curl g++ libpq-dev gcc cron && \
    rm -rf /var/lib/apt/lists/*

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

FROM base
WORKDIR /app/

ARG PDT_API_PORT=5000

RUN pip3 install --upgrade pip

COPY requirements/ requirements/

RUN pip3 install -r requirements/dev_unix.txt
COPY . .

ENV PORT=$PDT_API_PORT

# Add a cron job and start the cron service
COPY backend/scraper/crontab /etc/cron.d/scrape-cron
RUN chmod 0644 /etc/cron.d/scrape-cron
RUN crontab /etc/cron.d/scrape-cron
RUN touch /var/log/cron.log

CMD /wait && cron && tail -f /var/log/cron.log && ./run_dev.sh
