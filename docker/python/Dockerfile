FROM devlab-base

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-dev \
        python3-venv \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

USER dev

ENV PATH="/home/dev/.local/bin:${PATH}"

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /workspace

CMD [ "bash" ]