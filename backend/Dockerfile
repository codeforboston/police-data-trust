FROM python:3-slim-bookworm AS base

# Install dependencies
RUN apt-get update -y && apt-get install -y \
    curl \
    g++ \
    libpq-dev \
    gcc \
    python3-dev \
    libffi-dev \
    build-essential \
    rustc cargo \
    && rm -rf /var/lib/apt/lists/*

# Add docker-compose-wait (if still needed)
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait /wait
RUN chmod +x /wait

FROM base
WORKDIR /app/

RUN pip3 install --upgrade pip

COPY requirements/ requirements/
RUN pip3 install -r requirements/dev_unix.txt

COPY . .

ARG NPDI_API_PORT=5001
ENV NPDI_API_PORT=$NPDI_API_PORT
EXPOSE $NPDI_API_PORT

CMD /wait && ./run_dev.sh
