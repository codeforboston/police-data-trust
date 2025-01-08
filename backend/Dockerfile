FROM --platform=linux/arm64 python:3.11-slim-bookworm AS base

# Install dependencies
RUN apt-get update -y && apt-get install -y \
    curl \
    g++ \
    libpq-dev \
    gcc \
    python3-dev \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

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
