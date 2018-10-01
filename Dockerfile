FROM rootproject/root-ubuntu16
USER root

ADD . /phos
WORKDIR /phos

# Install/update the package manager
RUN apt-get update  -y
RUN apt-get install -y software-properties-common
RUN apt-add-repository -y universe
RUN apt-get update -y

# Setup python
RUN apt-get install -y python-pip
RUN pip install --upgrade pip