#!/bin/bash
cd ~
#nohup rstudio-server start > rstudio-server.out 2> rstudio-server.err &
#jupyter notebook --config /jupyter_notebook_config.py
#nohup jupyter notebook --config /jupyter_notebook_config.py > jupyter-notebook.out 2> jupyter-notebook.err &
nohup rstudio-server start > .rstudio-server.out 2> .rstudio-server.err &
jupyter notebook --config /jupyter_notebook_config.py
