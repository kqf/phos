FROM rootproject/root-ubuntu16
USER root

ADD . /phspace
WORKDIR /phspace

# Install/update the package manager
RUN apt-get update  -y
RUN apt-get install -y software-properties-common
RUN apt-add-repository -y universe
RUN apt-get update -y

# Setup python
RUN apt-get install -y python-pip
RUN apt-get install -y python

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .
