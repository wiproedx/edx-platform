FROM ubuntu:latest
RUN mkdir /edx/app/edxapp/edx-platform
WORKDIR /edx/app/edxapp/edx-platform
ADD . /edx/app/edxapp/edx-platform
RUN bash ./scripts/travis-install.sh