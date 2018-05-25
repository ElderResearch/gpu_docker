FROM eri_python:latest

# launch jupyter notebook and set up the port forwarding
EXPOSE 8888
WORKDIR /userhome
ENV HOME /userhome

# notebook config has to beinitialized, following the tensorflow docker folks'
# lead here
COPY jupyter_notebook_config.py /

CMD ["jupyter", "notebook", "--config=/jupyter_notebook_config.py"]
