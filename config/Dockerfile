FROM ubuntu:14.04
RUN apt-get -y   update 
RUN apt-get -y upgrade
RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN pip install alibuild

ENV HOME /home/sha
RUN useradd --create-home --home-dir $HOME sha \
    && chown -R sha:sha $HOME \
    && chown -R sha:sha /media \
    && usermod -a -G audio,video sha

RUN mkdir -p $HOME/alice
WORKDIR $HOME/alice
RUN apt-get -y install git
RUN aliBuild init AliRoot
RUN aliBuild init AliPhysics
RUN apt-get -y install libncurses5-dev
RUN apt-get -y install libperl-dev
RUN apt-get -y install curl libcurl4-gnutls-dev
RUN apt-get -y install bison flex
RUN apt-get -y install libbz2-dev libbz2-1.0 
RUN apt-get -y install freeglut3-dev
RUN apt-get -y install libx11-dev libxext-dev libxft-dev libxpm-dev

RUN aliDoctor AliRoot
