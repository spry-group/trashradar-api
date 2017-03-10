FROM python:3.5.3-alpine
MAINTAINER Martin Freytes "martin.freytes@spry-group.com"

# This Dockerfile builds the volume container from which all the compose containers
# will mount volumes.

# This build should.
#
#   1. Server
#   1.1. Create Virtual Environment
#   1.2. Install Dependencies
#   1.3. Run Tests


ADD . /code
WORKDIR /code

# set library paths for build.
ENV LIBRARY_PATH=/lib:/usr/lib

# sed command is a very temporary workaround pending making sure we can upgrade wheel everywhere.
RUN \
  apk update && \
  apk add \
    build-base \
    gcc \
    git \
    libffi \
    libffi-dev \
    libjpeg-turbo-dev \
    python-dev \
    postgresql-dev \
    libgdal-dev \
    zlib-dev && \
  ln -s /lib/libz.so.1 /usr/lib/ && \
  rm -rf /var/cache/apk/

#This allows a local user to mount their own git clone in place of the built one.
VOLUME /code
EXPOSE 80
