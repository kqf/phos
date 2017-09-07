FROM ubuntu:14.04
RUN apt-get -y update 
RUN apt-get -y upgrade

# Update repo to install gcc6
RUN apt-get -y install software-properties-common 
RUN add-apt-repository ppa:ubuntu-toolchain-r/test

RUN apt-get -y update 
RUN apt-get -y upgrade

RUN apt-get install -y gcc-6

RUN apt-get -y install python
RUN apt-get -y install python-pip
RUN pip install alibuild

RUN mkdir -p /alice
WORKDIR /alice
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



# Make ssh dir
RUN mkdir /root/.ssh/

# Copy over private key, and set permissions
ADD id_rsa /root/.ssh/id_rsa

# Create known_hosts
RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Build aliroot
RUN aliBuild build AliRoot


# Add keys to the aliphysics
WORKDIR /alice/AliPhysics
RUN git remote add kqf git@github.com:kqf/AliPhysics

RUN aliDoctor AliRoot
