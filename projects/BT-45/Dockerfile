FROM cupy/cupy

RUN python3 -m pip install -U pip setuptools

RUN python3 -m pip install \
	matplotlib \
	tqdm \
	libtiff \
	scipy \
	Pillow \
	scikit-learn \
	scikit-image \
	opencv-python \
	imgaug \
	IPython \
	geopandas \
	pandas \
	keras \
	imantics \
	simplification \
	chainer \
	jupyter \
	tensorflow-gpu \
	tensorboard \
	tensorboardX \
	sqlalchemy


RUN python3 -m pip --no-cache-dir install jupyterlab ipywidgets ipympl

RUN apt-get update && apt-get install -y vim git sqlite3 bc

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

# hack script to start both rstudio server and jupyter notebook
COPY starthack.sh /
CMD ["/starthack.sh"]


