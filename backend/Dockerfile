FROM python:3-slim-bookworm AS base

# Install dependencies
RUN apt-get update -y && apt-get install -y \
    curl \
    g++ \
    libpq-dev \
    gcc \
    python3-dev \
    libffi-dev

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"


ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait /wait
RUN chmod +x /wait


FROM base
WORKDIR /app/

ARG NPDI_API_PORT=5000

RUN pip3 install --upgrade pip

COPY requirements/ requirements/

RUN pip3 install -r requirements/dev_unix.txt
COPY . .

ENV PORT=$NPDI_API_PORT

CMD /wait && ./run_dev.sh

