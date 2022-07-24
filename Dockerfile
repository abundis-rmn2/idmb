FROM scratch

ARG DEBIAN_FRONTEND=noninteractive

# Install apt dependencies
RUN apt-get update && apt-get install -y \
    nano \
    git \
    wget

# Add new user to avoid running as root
RUN useradd --user-group --system --create-home --no-log-init idmb
USER idmb
WORKDIR /home/idmb

RUN python -m pip install -U pip
RUN python -m pip install instagrapi
