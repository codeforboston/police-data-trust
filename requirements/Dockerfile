# psycopg requires postgres development files in order to compile the
# requirements, so this image starts with the same image as the database
# containers and installs the same version of python as the api containers

FROM rust:slim-bookworm as base

RUN apt-get update && apt-get install -y \
    make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git

FROM base

SHELL ["bash", "-lc"]
RUN curl https://pyenv.run | bash && \
    echo 'export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc

ENV PYTHON_VERSION=3.13.0
RUN pyenv install ${PYTHON_VERSION} && pyenv global ${PYTHON_VERSION}
RUN pip install -U pip-tools

COPY . requirements/

CMD python requirements/update.py