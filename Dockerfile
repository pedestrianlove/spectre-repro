FROM ubuntu:16.04

RUN apt-get update -y && apt-get install -y build-essential

RUN mkdir -p /workspace
COPY . /workspace

WORKDIR /workspace
