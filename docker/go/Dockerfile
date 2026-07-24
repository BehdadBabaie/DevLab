FROM devlab-base

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        golang-go && \
    rm -rf /var/lib/apt/lists/*

USER dev

WORKDIR /workspace

CMD [ "bash" ]