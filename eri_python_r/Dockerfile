FROM eri_python:latest

# update the cran deb repo source
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/'

RUN apt-get update
RUN apt-get install -y --no-install-recommends default-jre default-jdk
RUN apt-get install -y --no-install-recommends r-base r-base-dev
RUN apt-get install -y --no-install-recommends \
    r-cran-boot \
    r-cran-class \
    r-cran-cluster \
    r-cran-codetools \
    r-cran-foreign \
    r-cran-kernsmooth \
    r-cran-lattice \
    r-cran-mass \
    r-cran-matrix \
    r-cran-mgcv \
    r-cran-nlme \
    r-cran-nnet \
    r-cran-rodbc \
    r-cran-rpart \
    r-cran-spatial \
    r-cran-survival

# stuff needed for the install of the more niche packages in install.R
RUN apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev

# now manually install a ton of stuff
COPY install.r /
# the make variable before inspired by this:
#  http://www.rexamine.com/2015/07/speeding-up-r-package-installation-process/
# could be doing something terrible.
#  y
#  o
#  l
#  o
RUN MAKE="make -j 8" Rscript /install.r

# rstudio install
RUN apt-get install -y --no-install-recommends gdebi-core wget \
    && wget -q https://download2.rstudio.org/rstudio-server-1.1.453-amd64.deb \
    && gdebi -n rstudio-server-1.1.453-amd64.deb

# setting up a stupid fucking user
RUN useradd rstudio \
    && echo "rstudio:rstudio" | chpasswd \
    && mkdir -p /home/rstudio \
    && chown rstudio:rstudio /home/rstudio \
    && mkdir -p /home/rstudio/.rstudio/monitored/user-settings \
    && echo 'alwaysSaveHistory="0"' > /home/rstudio/.rstudio/monitored/user-settings/user-settings \
    && echo 'loadRData="0"' >> /home/rstudio/.rstudio/monitored/user-settings/user-settings \
    && echo 'nsaveAction="0"' >> /home/rstudio/.rstudio/monitored/user-settings/user-settings \
    && chown -R rstudio:rstudio /home/rstudio/.rstudio

# install of r-cran-foreign up above installs python2.7 as a dependency, so it
# busts our python3 symlink. some bullshit
RUN rm /usr/bin/python \
    && ln -s /usr/bin/python3 /usr/bin/python

EXPOSE 8787

COPY starthack.sh /
RUN chmod +x /starthack.sh

CMD ["/starthack.sh"]
