FROM devlab-base

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

USER dev

ENV PATH="/home/dev/.local/bin:${PATH}"

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ARG PYTHON_VERSION=3.14

RUN uv python install ${PYTHON_VERSION} --default

WORKDIR /workspace

CMD [ "bash" ]
