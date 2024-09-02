FROM ubuntu:22.04

# docker build --platform=linux/amd64 -t labelmaker:latest .
# docker run --platform=linux/amd64 -it labelmaker:latest /bin/bash

# Run in non-interactive mode
ARG DEBIAN_FRONTEND=noninteractive

# Install core developer dependencies
RUN apt-get -y -m update && apt-get install -y build-essential wget autoconf git unzip python3 python3-pip

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda.sh &&\
    bash /miniconda.sh -b -p /miniconda &&\
    rm /miniconda.sh

# Add Miniconda to PATH
ENV PATH="/miniconda/bin:${PATH}"

# Install Mamba from Conda-Forge
RUN conda install pandas click python=3

# Install qrcode
RUN pip install qrcode[pil]

# Install Labelmaker
RUN git clone https://github.com/aomlomics/labelmaker

ARG DEBIAN_FRONTEND=noninteractive

# Update package lists and install texlive-base and texlive-latex-extra
RUN apt-get update && apt-get install -y \
    texlive-base \
    texlive-latex-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Default to labelmaker directory when entering container
WORKDIR "/labelmaker"
