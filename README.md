# gpu instance image dockerfiles

each directory in this repository is a separate context for a docker image, and collectively they define the dev and prod images we intend to use for gpu analytics on the gpu dev box in the DC office. the images themselves will (eventually) be built automatically, but they will always live on the gpu box (and hopefully dockerhub, soon).

## layers

there are several images that are simple layers on top of other images, so here's a brief rundown of the ones we have defined so far

1. [`lambdastack`](https://github.com/ElderResearch/gpu_docker/blob/master/lambdastack/Dockerfile)
    1. this is simply a very basic `ubuntu:16.04` image with the `lambdastack` repositories installed on top of it as described [here](https://lambdal.com/lambda-stack-deep-learning-software).
2. [`eri_python`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_python/Dockerfile)
    1. installs the most commonly used `python` libraries into an existing `lambdastack` image
3. [`eri_dev`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_dev/Dockerfile)
    1. a development environment with the primary development access points / services up and running (e.g. a `jupyter notebook` server running on an exposed port, `rstudio` on another), as well as basic volume mounting for shared data


## making updates without automation

basically, run andrew's build script:

``` sh
./build.sh
```

### old instructions

until we have set up a nightly or automated build, please take care to increment versions on images and tag things appropriately. we should be able to rebuild all images based on some overall `git` version tag someday, but not today!

for now the process should be roughly as follows: for each image in the dependency chain of the "innermost" docker image you have updated,

1. `docker build --no-cache -t IMAGE_TAG_NAME .`
1. `docker tag NEWSHANUMBER IMAGE_TAG_NAME:vX.Y.Z`
