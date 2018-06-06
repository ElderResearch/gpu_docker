#!/bin/bash
NEWPW=${PASSWORD:-rstudio}
echo "rstudio:${PASSWORD}" | chpasswd
rstudio-server start
while true; do sleep 1000; done
