# gpu instance image dockerfiles

each directory in this repository is a separate context for a docker image. These images allow users of our gpu box to launch isolated docker containers, with GPUs attached, for the ultimate experience in computation<sup>TM</sup>. The images are regularly re-built and live on the gpu box (and hopefully dockerhub, soon).

## layers

there are several images that are simple layers on top of other images, so here's a brief rundown of the ones we have defined so far:

1. [`tensorflow`](https://hub.docker.com/r/tensorflow/tensorflow/tags)
 - The official `tensorflow` Docker images, as defined [here](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/dockerfiles)
2. [`eri_python`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_python/Dockerfile)
 - starts with the `tensorflow` base image and installs the most commonly used `python` libraries
3. [`eri_dev`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_dev/Dockerfile)
 - a development environment baesd on `eri_dev` with a `jupyter lab` server running on an exposed port, as well as basic volume mounting for shared data
4. [`eri_python_r`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_python_r/Dockerfile)
 - installs `Rstudio` and the most commonly used `R` libraries on top of the `eri_python` image
5. [`eri_dev_p_r`](https://github.com/ElderResearch/gpu_docker/blob/master/eri_dev_p_r/Dockerfile)
 - a development environment based on `eri_python_r` with a `jupyter lab` server and an `Rstudio` server running on exposed ports, as well as basic volume mounting for shared data

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
