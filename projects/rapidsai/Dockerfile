FROM rapidsai/rapidsai:cuda10.0-runtime-ubuntu18.04

EXPOSE 8888

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


