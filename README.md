# gpu instance image dockerfiles

each directory in this repository is a separate context for a docker image, and collectively they define the dev and prod images we intend to use for gpu analytics on the gpu dev box in the DC office. the images themselves will (eventually) be built automatically, but they will always live on the gpu box (and hopefully dockerhub, soon).

## layers

there are several images that are simple layers on top of other images, so here's a brief rundown of the ones we have defined so far

1. [`lambdastack`](https://github.com/ElderResearch/gpu_docker/blob/master/lambdastack/Dockerfile) (deprecated)
 - this is simply a very basic `ubuntu:16.04` image with the `lambdastack` repositories installed on top of it as described [here](https://lambdal.com/lambda-stack-deep-learning-software).
2. [`eri_python`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_python/Dockerfile)
 - installs the most commonly used `python` libraries into a [`tensorflow/tensorflow`](https://hub.docker.com/r/tensorflow/tensorflow) base image
3. [`eri_dev`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_dev/Dockerfile)
 - a development environment with a `jupyter notebook` server running on an exposed port, as well as basic volume mounting for shared data
4. [`eri_python_r`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_python_r/Dockerfile)
 - installs `Rstudio` and the most commonly used `R` libraries into an existing `eri_python` image
5. [`eri_dev_p_r`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_dev_p_r/Dockerfile)
 - a development environment with a `jupyter notebook` server and an `Rstudio` server running on exposed ports, as well as basic volume mounting for shared data

## making updates without automation

basically, run andrew's build script:

```sh
python3 build.py
```

the build script has a few optional arguments to configure different build parameters. access the help menu for more info:

```sh
python3 build.py --help
```

rotating build logs are saved to `/var/log/gpu_docker/build.log` (with fallback `./logs/build.log`) to aid in debugging failed builds.

### old instructions

until we have set up a nightly or automated build, please take care to increment versions on images and tag things appropriately. we should be able to rebuild all images based on some overall `git` version tag someday, but not today!

for now the process should be roughly as follows: for each image in the dependency chain of the "innermost" docker image you have updated,

1. `docker build --no-cache -t IMAGE_TAG_NAME .`
1. `docker tag NEWSHANUMBER IMAGE_TAG_NAME:vX.Y.Z`
