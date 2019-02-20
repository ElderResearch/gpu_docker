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

if [[ $? -ne 0 ]]; then
  echo "ERROR: There was an error building the eri_python image"
fi

echo "rebuilding base python + r image"
cd ${BASEDIR}/eri_python_r/ \
    && docker build ${NO_CACHE} -t eri_python_r .

if [[ $? -ne 0 ]]; then
  echo "ERROR: There was an error building the eri_python_r image"
fi

echo "rebuilding dev python images"
cd ${BASEDIR}/eri_dev/ \
    && docker build ${NO_CACHE} -t eri_dev .

if [[ $? -ne 0 ]]; then
  echo "ERROR: There was an error building the eri_dev image"
fi

echo "rebuilding dev python + r image"
cd ${BASEDIR}/eri_dev_p_r/ \
    && docker build ${NO_CACHE} -t eri_dev_p_r .

if [[ $? -ne 0 ]]; then
  echo "ERROR: There was an error building the eri_dev_p_r image"
fi
