FROM ubuntu:bionic

ARG DOCKER_COMPOSE_VERSION

RUN set -xe && \
    apt-get update -y && \
    apt-get -y install util-linux coreutils ca-certificates curl docker.io && \
    apt-get install -y python3-pip && \
    apt-get install -y python3.7-venv && \
    rm -rf /var/lib/apt/lists/* && \
    curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

RUN set -xe && \
    python3.7 -m pip install pipx && \
    python3.7 -m pipx ensurepath

CMD ["/bin/bash"]