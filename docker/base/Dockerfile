# ============================================================================
# DevLab Base Image
# Common development environment shared by all language images.
# ============================================================================

ARG DEBIAN_VERSION=bookworm

FROM debian:${DEBIAN_VERSION}

ARG DEBIAN_MIRROR

ENV DEBIAN_MIRROR=${DEBIAN_MIRROR}

ENV DEBIAN_FRONTEND=noninteractive

COPY docker/scripts/configure-apt.sh /usr/local/bin/configure-apt.sh

RUN chmod +x /usr/local/bin/configure-apt.sh && \
    configure-apt.sh && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        less \
        vim \
        nano \
        procps \
        tree \
        unzip \
        wget \
        zip && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 dev && \
    useradd --uid 1000 --gid dev --create-home --shell /bin/bash dev

WORKDIR /workspace

USER dev

CMD [ "bash" ]