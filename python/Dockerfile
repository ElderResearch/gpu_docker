FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

LABEL creator="Andrew Stewart <andrew.stewart@elderresearch.com>"

ARG DEBIAN_FRONTEND=noninteractive
ARG CONDA_DIR=/opt/conda

ENV PATH $CONDA_DIR/bin:$PATH
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${CUDA_HOME}/lib64
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/usr/local/lib
ENV OPENCL_LIBRARIES /usr/local/cuda/lib64
ENV OPENCL_INCLUDE_DIR /usr/local/cuda/include
ENV OMPI_MCA_opal_cuda_support true

RUN apt update && apt -y upgrade 
RUN apt install -y locales
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN update-locale LANG=en_US.UTF-8

# Install basic packages and some build dependencies
RUN apt install -y --no-install-recommends \
    build-essential \
    bzip2 \
    ca-certificates \
    cmake \
    curl \
    gcc \
    g++ \
    git \
    graphviz \
    krb5-user \
    less \
    libboost-dev \
    libboost-system-dev \
    libboost-filesystem-dev \
    libglib2.0-0 \
    libicu-dev \
    libpq-dev \
    libsm6 \
    libxext6 \
    libxrender1 \
    openssh-server \
    swig \
    unixodbc-dev \
    vim \
    wget


# Add Microsoft repository for mssql
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
        && curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install mssql drivers
RUN apt update && ACCEPT_EULA=Y apt install -y --no-install-recommends msodbcsql17

# Install Miniconda
RUN echo "export PATH=$CONDA_DIR/bin:"'$PATH' > /etc/profile.d/conda.sh \
    && wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR \
    && rm /tmp/miniconda.sh \
    && conda config --set always_yes yes --set changeps1 no \
    && conda config --append channels conda-forge

# Install LightGBM
RUN mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

RUN cd /usr/local/src \
    && mkdir lightgbm \
    && cd lightgbm \
    && git clone --recursive --branch stable --depth 1 https://github.com/microsoft/LightGBM \
    && cd LightGBM \
    && mkdir build \
    && cd build \
    && cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/local/cuda/lib64/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda/include/ .. \
    && make OPENCL_HEADERS=/usr/local/cuda/targets/x86_64-linux/include LIBOPENCL=/usr/local/cuda/targets/x86_64-linux/lib

ENV PATH /usr/local/csr/lightgbm/LightGBM:${PATH}

RUN cd /usr/local/src/lightgbm/LightGBM/python-package \
    && python setup.py install --precompile


# Install all the Python goodies
COPY environment.yml .
RUN conda env create

# Cleanup
RUN apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && conda clean -a -y

# Install tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# expose jupyter lab and set up the port forwarding
EXPOSE 8888

# expose tensorboard and set up the port forwarding
EXPOSE 8008

# jupyter lab config has to be initialized, following the tensorflow docker folks'
# lead here
COPY jupyter_notebook_config.py /

# make bash the default shell
RUN chsh -s /bin/bash
ENV SHELL /bin/bash

# try to enforce eri data directory locations
ENV SCIKIT_LEARN_DATA /data

# hack script to start jupyter notebook
COPY starthack.sh /
RUN chmod 755 /starthack.sh

ENTRYPOINT ["/tini", "--"]
CMD ["/starthack.sh"]