# based almost entirely off of the tensorflow/tensorflow gpu-based docker image,
# with slight tweaks for our personal use
FROM tensorflow/tensorflow:1.12.0-gpu-py3

LABEL maintainer="Zach Lamberty <zach.lamberty@elderresearch.com>"

RUN apt update && apt -y install locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get install -y openssh-server swig unixodbc-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# generic pip installs of all the most basic bad lads
# separating out expensive installations just for some caching love
RUN pip --no-cache-dir install spacy
RUN pip --no-cache-dir install mxnet-cu90

# install dependencies for smac
RUN pip --no-cache-dir install \
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
RUN pip --no-cache-dir install \
        boto3 \
        cssselect \
        gensim \
        ipykernel \
        jupyter \
        jupyter-tensorboard \
        keras \
        lxml \
        matplotlib \
        neo4j-driver \
        networkx \
        nltk \
        numba \
        Pillow \
        plotly \
        psycopg2 \
        pyarrow \
	pyodbc \
        requests \
        seaborn \
        smac \
        spacy \
        sqlalchemy \
        tables \
        tqdm \
        xlrd

# pytorch is also special, install from a wheel on their webpage
RUN pip --no-cache-dir install http://download.pytorch.org/whl/cu90/torch-1.0.0-cp35-cp35m-linux_x86_64.whl
RUN pip install torchvision

# onnx requires some additional *nix libraries
RUN apt-get update && \
    apt-get install --no-install-recommends -y protobuf-compiler libprotoc-dev
RUN ONNX_ML=1 pip --no-cache-dir install onnx

# ipython kernel
RUN python -m ipykernel.kernelspec

# finally, not python stuff, but I want the following stuff to be generally
# available in all downstream images
RUN apt-get install --no-install-recommends -y less git vim

# install spacy `en` model and set relevant environment variables
# c.f. https://github.com/explosion/spaCy/issues/1721
RUN python -m spacy download en

# download some of the nltk libraries
#RUN python -m nltk.downloader all
RUN python -m nltk.downloader punkt

# the numba install gets its own special environment variables
ENV NUMBAPRO_NVVM /usr/local/cuda-9.0/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE /usr/local/cuda-9.0/nvvm/libdevice/


# install darknet (in stages) --------------------------------------------------
# 1. get code
RUN cd /opt && \
    git clone https://github.com/pjreddie/darknet.git

WORKDIR /opt/darknet

# 2. change gpu flag with the best editor, sed
RUN sed -i -e 's/GPU=0/GPU=1/' Makefile

# 3. install other dependencies (header files)
RUN apt-get install --no-install-recommends -y cuda-curand-dev-9-0 \
                                               cuda-cublas-dev-9-0

# 4. make and move
RUN make
RUN mv darknet /usr/local/bin

# 5. uninstall that stupid header stuff
RUN apt-get remove -y cuda-curand-dev-9-0 \
                      cuda-cublas-dev-9-0

# 6. clean up
WORKDIR /

# end darknet install ----------------------------------------------------------

# install gsl
RUN apt-get install --no-install-recommends -y libgsl-dev
