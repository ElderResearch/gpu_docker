FROM eri_python:latest

# notebook config has to beinitialized, following the tensorflow docker folks' lead here
COPY jupyter_notebook_config.py /root/.jupyter/

# launch jupyter notebook and set up the port forwarding
EXPOSE 8888

CMD ["jupyter", "notebook", "--allow-root", "--ip=*", "--no-browser"]
