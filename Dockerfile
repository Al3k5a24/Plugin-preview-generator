FROM ubuntu:22.04

# Instaliraj osnovne alate
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    nodejs npm \
    golang \
    dotnet-sdk-6.0 \
    curl git \
    && apt-get clean

# Node.js symlink (neki image-ovi imaju nodejs, ali ne i node)
RUN ln -s /usr/bin/nodejs /usr/bin/node || true

WORKDIR /app