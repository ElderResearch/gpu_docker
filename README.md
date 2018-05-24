# gpu instance image dockerfiles

each directory in this repository is a separate context for a docker image, and collectively they define the dev and prod images we intend to use for gpu analytics on the gpu dev box in the DC office. the images themselves will (eventually) be built automatically, but they will always live on the gpu box (and hopefully dockerhub, soon).

## layers

there are several images that are simple layers on top of other images, so here's a brief rundown of the ones we have defined so far

1. `lambdastack`
    1. this is simply a very basic `ubuntu:16.04` image with the `lambdastack` repositories installed on top of it as described [here](https://lambdal.com/lambda-stack-deep-learning-software).
2. `eri_python`
    1. installs the most commonly used `python` libraries into an existing `lambdastack` image
3. `eri_dev`
    1. a development environment with the primary development access points / services up and running (e.g. a `jupyter notebook` server running on an exposed port, `rstudio` on another), as well as basic volume mounting for shared data 
