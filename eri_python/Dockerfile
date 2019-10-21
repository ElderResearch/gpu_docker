# based almost entirely off of the tensorflow/tensorflow gpu-based docker image,
# with slight tweaks for our personal use
FROM tensorflow/tensorflow:1.14.0-gpu-py3

LABEL creator="Zach Lamberty <zach.lamberty@elderresearch.com>"
LABEL maintainer="Andrew Stewart <andrew.stewart@elderresearch.com>"

ARG DEBIAN_FRONTEND=noninteractive

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt update && apt -y install locales
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && /usr/sbin/update-locale LANG=en_US.UTF-8

# add microsoft repository for mssql
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
        && curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install mssql drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN apt-get install -y openssh-server swig unixodbc-dev libpq-dev \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends krb5-user \
	&& apt-get install -y graphviz libicu-dev

# install nodejs
RUN apt-get install -y software-properties-common \
    && curl -sL https://deb.nodesource.com/setup_10.x | bash - \
    && apt-get install -y nodejs \
    && apt-get purge -y python-software-properties

# generic pip installs of all the most basic bad lads
# separating out expensive installations just for some caching love
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip --no-cache-dir install spacy
RUN python3 -m pip --no-cache-dir install mxnet-cu100

# install dependencies for smac
RUN python3 -m pip --no-cache-dir install pybind11 \
    && python3 -m pip --no-cache-dir install \
    	ConfigSpace \
    	emcee \
    	george \
    	joblib \
    	psutil \
    	pyDOE \
    	pyrfr \
    	sobol_seq \
    	statsmodels

# and now the rest
RUN python3 -m pip --no-cache-dir install \
        boto3 \
        cssselect \
        dask \
        gensim \
        ipykernel \
        jupyter \
        keras \
        lxml \
        matplotlib \
        neo4j-driver \
        netcdf4 \
        networkx \
        nltk \
        numba \
        opencv-contrib-python \
        Pillow \
        plotly \
        psycopg2 \
        pyarrow \
        pyproj \
        pyodbc \
        rasterio \
        requests \
        richdem \
        seaborn \
        smac \
        spacy \
        sqlalchemy \
        tables \    
        toolz \
        tqdm \
        virtualenv \
        xarray \
        xlrd

# install lightgbm
RUN apt-get update && apt-get install -y cmake \
	ocl-icd-libopencl1 \
	ocl-icd-opencl-dev \
	libboost-dev \
	libboost-system-dev \
	libboost-filesystem-dev

RUN python3 -m pip install lightgbm --install-option=--gpu

# install GDAL

RUN apt-get update && apt-get install -y gdal-bin libgdal-dev 
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
RUN python3 -m pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"  

RUN python3 -m pip --no-cache-dir install jupyterlab ipywidgets ipympl \
    && jupyter nbextension enable --py --sys-prefix widgetsnbextension \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
    && jupyter labextension install @jupyterlab/plotly-extension \
    && jupyter labextension install jupyter-matplotlib

# pytorch is also special, install from a wheel on their webpage
RUN pip --no-cache-dir install torch==1.2.0 torchvision

# onnx requires some additional *nix libraries
RUN apt-get update && \
    apt-get install --no-install-recommends -y protobuf-compiler libprotoc-dev
RUN ONNX_ML=1 pip --no-cache-dir install onnx

# ipython kernel
RUN python3 -m ipykernel.kernelspec

# finally, not python stuff, but I want the following stuff to be generally
# available in all downstream images
RUN apt-get install --no-install-recommends -y less git vim

# install spacy `en` model and set relevant environment variables
# c.f. https://github.com/explosion/spaCy/issues/1721
RUN python3 -m spacy download en
RUN python3 -m spacy download en_core_web_lg

# download some of the nltk libraries
#RUN python -m nltk.downloader all
RUN python3 -m nltk.downloader punkt

# the numba install gets its own special environment variables
ENV NUMBAPRO_NVVM /usr/local/cuda-10.0/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE /usr/local/cuda-10.0/nvvm/libdevice/


# install darknet (in stages) --------------------------------------------------
# 1. get code
RUN cd /opt && \
    git clone https://github.com/pjreddie/darknet.git

WORKDIR /opt/darknet

# 2. change gpu flag with the best editor, sed
RUN sed -i -e 's/GPU=0/GPU=1/' Makefile
RUN sed -i -e 's/# ARCH= -gencode arch=compute_52,code=compute_52/ARCH= -gencode arch=compute_70,code=compute_70/' Makefile

# 3. install other dependencies (header files)
RUN apt-get install --no-install-recommends -y cuda-curand-dev-10-0 \
                                               cuda-cublas-dev-10-0

# 4. make and move
RUN ln -s /usr/local/cuda/compat/libcuda.so /usr/local/cuda/lib64/libcuda.so
RUN make
RUN mv darknet /usr/local/bin

# 5. uninstall that stupid header stuff
RUN apt-get remove -y cuda-curand-dev-10-0 \
                      cuda-cublas-dev-10-0

# 6. clean up
WORKDIR /

# end darknet install ----------------------------------------------------------

# install gsl
RUN apt-get install --no-install-recommends -y libgsl-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && rm -rf /usr/share/python-wheels/ \
        && rm -rf /root/.cache/
