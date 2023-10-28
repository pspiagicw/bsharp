FROM ubuntu:latest

RUN useradd -mG video,audio,wheel build && apt install python3 python3-pip python-is-python3 pipx tree

USER build
WORKDIR /home/build
