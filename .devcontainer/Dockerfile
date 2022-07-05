FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.10-bullseye

# Pre-install packages into container
COPY requirements.txt /tmp/pip-tmp/
RUN echo '\nipykernel' >> /tmp/pip-tmp/requirements.txt \
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp