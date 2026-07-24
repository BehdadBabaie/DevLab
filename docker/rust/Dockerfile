FROM devlab-base

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

USER dev

ENV PATH="/home/dev/.cargo/bin:${PATH}"

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

WORKDIR /workspace

CMD [ "bash" ]