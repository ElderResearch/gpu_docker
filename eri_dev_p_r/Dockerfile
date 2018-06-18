# to create a container using this image:
#
# NV_GPU=1 nvidia-docker run \
#   --rm \
#   -it \
#   -p 8889:8888 \
#   -p 8787:8787 \
#   -v /etc/group:/etc/group:ro \
#   -v /etc/passwd:/etc/passwd:ro \
#   -v /home/zlamberty:/userhome:rw \
#   -v /data:/data:rw \
#   -u $( id -u $USER ):$( id -g $USER ) \
#   -e USER=$USER
#   -e PASSWORD=$PASSWORD
#   eri_dev_p_r
#
# obviously, replace the `-u` and `-e` lines above with desired user information

FROM eri_python_r:latest

# expose jupyter notebook and set up the port forwarding
EXPOSE 8888
EXPOSE 8787

# notebook config has to beinitialized, following the tensorflow docker folks'
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
