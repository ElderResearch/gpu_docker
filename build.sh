#!/bin/bash

NO_CACHE=''
BASEDIR="`pwd`"

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --no-cache)
    NO_CACHE=$key
    shift
    ;;
    *)
esac
done

echo "checking for updates to ultimate base images"
docker pull tensorflow/tensorflow:latest-gpu-py3

echo "rebuilding base python image"
cd ${BASEDIR}/eri_python/ \
    && docker build ${NO_CACHE} -t eri_python .

echo "rebuilding base python + r image"
cd ${BASEDIR}/eri_python_r/ \
    && docker build ${NO_CACHE} -t eri_python_r .

echo "rebuilding dev and prod python images"
cd ${BASEDIR}/eri_dev/ \
    && docker build ${NO_CACHE} -t eri_dev \
    -t eri_nogpu_dev -t eri_prod .

echo "rebuilding dev and prod python + r image"
cd ${BASEDIR}/eri_dev_p_r/ \
    && docker build ${NO_CACHE} -t eri_dev_p_r \
    -t eri_nogpu_dev_p_r -t eri_prod_p_r .
