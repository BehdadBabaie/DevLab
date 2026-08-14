FROM devlab-base

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

USER dev

ENV PATH="/home/dev/.cargo/bin:${PATH}"

ARG RUST_VERSION=1.89.0

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y \
    --default-toolchain ${RUST_VERSION}

WORKDIR /workspace

CMD [ "bash" ]
