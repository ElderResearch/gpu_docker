# to create a container using this image:
#
# docker run \
#   --runtime nvidia \
#   -e NVIDIA_VISIBLE_DEVICES=0 \
#   --rm \
#   -it \
#   -p 8889:8888 \
#   -v /etc/group:/etc/group:ro \
#   -v /etc/passwd:/etc/passwd:ro \
#   -v /home/zlamberty:/home/zlamberty:rw \
#   -v /data:/data:rw \
#   -u $( id -u $USER ):$( id -g $USER ) \
#   -e PASSWORD=test
#   eri_dev
#
# obviously, replace the `-u` line above with desired user information

FROM eri_python:latest

# expose jupyter lab and set up the port forwarding
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
