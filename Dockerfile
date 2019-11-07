FROM rootproject/root-ubuntu16
USER root

ADD . /phos
WORKDIR /phos/neutral-meson-spectra

# Install/update the package manager
RUN apt-get update  -y
RUN apt-get install -y software-properties-common
RUN apt-add-repository -y universe
RUN apt-get update -y

# Setup python
RUN apt-get install -y python-pip
RUN apt-get install -y python-tk # required by seaborn
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
