ARG PYTORCH_VERSION="22.06-py3"
FROM nvcr.io/nvidia/pytorch:${PYTORCH_VERSION}

ARG SPACY_PIPELINE="en_core_web_lg"

RUN bash -c "$(curl -fsSL "https://raw.githubusercontent.com/microsoft/vscode-dev-containers/main/script-library/common-debian.sh")" -- "true" "${USERNAME}" "${USER_UID}" "${USER_GID}" "true" "true" "true"  && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install the linters, black, and all the requirements in the requirements.txt
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install flake8 black pylint ipykernel \ 
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && python -m spacy download ${SPACY_PIPELINE} \
    && rm -rf /tmp/pip-tmp