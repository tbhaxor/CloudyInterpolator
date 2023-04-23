FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install required packages
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | tee /usr/share/keyrings/yarnkey.gpg >/dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get install -y --no-install-recommends --no-install-suggests nodejs yarn libffi-dev libpq-dev postgresql-client postgresql libhdf5-dev libopenmpi-dev openmpi-bin git gcc g++

# Install poetry
RUN pip install --no-cache-dir -qU pip poetry