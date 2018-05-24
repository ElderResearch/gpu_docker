FROM ubuntu:16.04

# stupid effing everything
#ENV DEBIAN_FRONTEND noninteractive

# fixing stupid proxy awfulness issues
COPY ./99fixbadproxy /etc/apt/apt.conf.d/99fixbadproxy
RUN rm -rf /var/lib/apt/lists/*

# test suite
RUN mkdir /tests/
COPY ./tests /tests/

# lambda-stack install instructions (OLD)
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A53D8F269E8A5A13
#RUN echo "deb http://archive.lambdalabs.com/ubuntu xenial main" >> /etc/apt/sources.list
#RUN apt-get update
#RUN echo "cudnn cudnn/license_preseed select ACCEPT" | debconf-set-selections
#RUN apt-get install --no-install-recommends --yes lambda-stack-cuda
#RUN apt-get upgrade --no-install-recommends --yes

# lambda-stack install instructions (NEW)
RUN apt-get update
RUN apt-get install --no-install-recommends --yes apt-utils
RUN apt-get install --yes wget
RUN apt-get install --no-install-recommends --yes lsb-release
RUN wget -q -O /lambda-stack-repo.deb https://lambdal.com/static/files/lambda-stack-repo.deb
RUN dpkg -i /lambda-stack-repo.deb
RUN rm /lambda-stack-repo.deb
RUN apt-get update

RUN echo "cudnn cudnn/license_preseed select ACCEPT" | debconf-set-selections
RUN echo "keyboard-configuration keyboard-configuration/variant select English (US)" | debconf-set-selections
RUN echo "keyboard-configuration keyboard-configuration/layout select English (US)" | debconf-set-selections

RUN apt-get install --no-install-recommends --yes libcudnn7
RUN apt-get install --no-install-recommends --yes lambda-stack-cuda

# fixing pytorch
#RUN apt-get install --no-install-recommends --yes python3-pip
#RUN pip3 install --upgrade pip
#RUN pip3 install http://download.pytorch.org/whl/cu91/torch-0.4.0-cp35-cp35m-linux_x86_64.whl
#RUN pip3 install torchvision
