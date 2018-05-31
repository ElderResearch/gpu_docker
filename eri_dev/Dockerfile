# to create a container using this image:
#
# NV_GPU=1 nvidia-docker run \
#   --rm \
#   -it \
#   -p 8889:8888 \
#   -v /etc/group:/etc/group:ro \
#   -v /etc/passwd:/etc/passwd:ro \
#   -v /home/zlamberty:/userhome:rw \
#   -v /data:/data:rw \
#   -u $( id -u $USER ):$( id -g $USER ) \
#   eri_dev
#
# obviously, replace the `-u` line above with desired user information

FROM eri_python:latest

# expose jupyter notebook and set up the port forwarding
EXPOSE 8888
WORKDIR /userhome
ENV HOME /userhome

# notebook config has to beinitialized, following the tensorflow docker folks'
# lead here
COPY jupyter_notebook_config.py /

CMD ["jupyter", "notebook", "--config=/jupyter_notebook_config.py"]
