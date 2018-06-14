# based almost entirely off of the tensorflow/tensorflow gpu-based docker image,
# with slight tweaks for our personal use
FROM tensorflow/tensorflow:latest-gpu-py3

LABEL maintainer="Zach Lamberty <zach.lamberty@elderresearch.com>"

# generic pip installs of all the most basic bad lads
# separating out expensive installations just for some caching love
RUN pip --no-cache-dir install spacy
RUN pip --no-cache-dir install mxnet-cu90

# and now the rest
RUN pip --no-cache-dir install \
        boto3 \
        cssselect \
        gensim \
        ipykernel \
        jupyter \
        keras \
        lxml \
        matplotlib \
        neo4j-driver \
        networkx \
        nltk \
        Pillow \
        plotly \
        psycopg2 \
        requests \
        seaborn \
        spacy \
        sqlalchemy \
        tables \
        tqdm \
        xlrd

# pytorch is also special, install from a wheel on their webpage
RUN pip --no-cache-dir install http://download.pytorch.org/whl/cu90/torch-0.4.0-cp35-cp35m-linux_x86_64.whl
RUN pip install torchvision

# ipython kernel
RUN python -m ipykernel.kernelspec
