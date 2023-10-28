FROM ubuntu:latest

RUN useradd -mG video,audio jenkins
RUN apt install python3 python3-pip python-is-python3 pipx tree

USER jenkins
WORKDIR /home/jenkins
