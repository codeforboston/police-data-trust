FROM debian:bookworm-slim

# Install packages required to build Python and extensions
RUN apt-get update && apt-get install -y \
    curl wget git make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev llvm libncursesw5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev ca-certificates \
    libopenblas-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo for packages requiring Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install pyenv
RUN curl https://pyenv.run | bash && \
    echo 'export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc

ENV PYTHON_VERSION=3.11
SHELL ["bash", "-lc"]

# Install the specified Python version via pyenv
RUN pyenv install ${PYTHON_VERSION} && pyenv global ${PYTHON_VERSION}

# Upgrade pip and install pip-tools
RUN pip install --no-cache-dir -U pip pip-tools

# Copy requirements directory and run the update script
COPY . requirements/

CMD python requirements/update.py
