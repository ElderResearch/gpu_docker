#!/bin/bash
cd ~

# to register the kernel in the current R installation
R -e "IRkernel::installspec()"

# start Rstudio and Jupyter Lab
nohup rstudio-server start > .rstudio-server.out 2> .rstudio-server.err &
jupyter lab --config /jupyter_notebook_config.py
