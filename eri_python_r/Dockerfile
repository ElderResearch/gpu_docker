FROM eri_python:latest

# update the cran deb repo source
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9
RUN echo deb http://cran.revolutionanalytics.com/bin/linux/ubuntu xenial/ > /etc/apt/sources.list.d/cran.list

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
    r-cran-rjava \
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
RUN Rscript /install.r

# rstudio install, ignore the one below
RUN apt-get install -y --no-install-recommends gdebi-core wget \
    && wget -q https://download2.rstudio.org/rstudio-server-1.1.453-amd64.deb \
    && gdebi -n rstudio-server-1.1.453-amd64.deb

# setting up a stuipd fucking user
RUN useradd rstudio \
    && echo "rstudio:rstudio" | chpasswd \
    && mkdir -p /home/rstudio \
    && chown rstudio:rstudio /home/rstudio \
    && mkdir -p /home/rstudio/.rstudio/monitored/user-settings \
    && echo 'alwaysSaveHistory="0"' > /home/rstudio/.rstudio/monitored/user-settings/user-settings \
    && echo 'loadRData="0"' >> /home/rstudio/.rstudio/monitored/user-settings/user-settings \
    && echo 'nsaveAction="0"' >> /home/rstudio/.rstudio/monitored/user-settings/user-settings \
    && chown -R rstudio:rstudio /home/rstudio/.rstudio

# rstudio install, stolen shamelessly from
# https://github.com/rocker-org/rocker-versioned/blob/master/rstudio/Dockerfile
#ENV PATH=/usr/lib/rstudio-server/bin:$PATH
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends \
#        file \
#        git \
#        libapparmor1 \
#        libcurl4-openssl-dev \
#        libedit2 \
#        libssl-dev \
#        lsb-release \
#        psmisc \
#        python-setuptools \
#        sudo \
#        wget \
#    && wget -q -O libssl1.0.0.deb http://ftp.debian.org/debian/pool/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u7_amd64.deb \
#    && dpkg -i libssl1.0.0.deb \
#    && rm libssl1.0.0.deb \
#    && RSTUDIO_LATEST=$(wget --no-check-certificate -qO- https://s3.amazonaws.com/rstudio-server/current.ver) \
#    && [ -z "$RSTUDIO_VERSION" ] && RSTUDIO_VERSION=$RSTUDIO_LATEST || true \
#    && wget -q http://download2.rstudio.org/rstudio-server-${RSTUDIO_VERSION}-amd64.deb \
#    && dpkg -i rstudio-server-${RSTUDIO_VERSION}-amd64.deb \
#    && rm rstudio-server-*-amd64.deb \
#    ## Symlink pandoc & standard pandoc templates for use system-wide
#    && ln -s /usr/lib/rstudio-server/bin/pandoc/pandoc /usr/local/bin \
#    && ln -s /usr/lib/rstudio-server/bin/pandoc/pandoc-citeproc /usr/local/bin \
#    && git clone https://github.com/jgm/pandoc-templates \
#    && mkdir -p /opt/pandoc/templates \
#    && cp -r pandoc-templates*/* /opt/pandoc/templates && rm -rf pandoc-templates* \
#    && mkdir /root/.pandoc && ln -s /opt/pandoc/templates /root/.pandoc/templates \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/ \
#    ## RStudio wants an /etc/R, will populate from $R_HOME/etc
#    && mkdir -p /etc/R \
#    ## Write config files in $R_HOME/etc
#    && echo '\n\
#            \n# Configure httr to perform out-of-band authentication if HTTR_LOCALHOST \
#            \n# is not set since a redirect to localhost may not work depending upon \
#            \n# where this Docker container is running. \
#            \nif(is.na(Sys.getenv("HTTR_LOCALHOST", unset=NA))) { \
#            \n  options(httr_oob_default = TRUE) \
#            \n}' >> /etc/R/Rprofile.site \
#    && echo "PATH=${PATH}" >> /etc/R/Renviron \
#    ## Need to configure non-root user for RStudio
#    && useradd rstudio \
#    && echo "rstudio:rstudio" | chpasswd \
#    && mkdir /home/rstudio \
#    && chown rstudio:rstudio /home/rstudio \
#    && addgroup rstudio staff \
#    ## Prevent rstudio from deciding to use /usr/bin/R if a user apt-get
#    ## installs a package
#    #&&  echo 'rsession-which-r=/usr/local/bin/R' >> /etc/rstudio/rserver.conf \
#    ## use more robust file locking to avoid errors when using shared volumes:
#    && echo 'lock-type=advisory' >> /etc/rstudio/file-locks \
#    ## configure git not to request password each time
#    && git config --system credential.helper 'cache --timeout=3600' \
#    && git config --system push.default simple \
#    ## Set up S6 init system
#    && wget -P /tmp/ https://github.com/just-containers/s6-overlay/releases/download/v1.11.0.1/s6-overlay-amd64.tar.gz \
#    && tar xzf /tmp/s6-overlay-amd64.tar.gz -C / \
#    && mkdir -p /etc/services.d/rstudio \
#    && echo '#!/usr/bin/with-contenv bash \
#          \n exec /usr/lib/rstudio-server/bin/rserver --server-daemonize 0' \
#          > /etc/services.d/rstudio/run \
#    && echo '#!/bin/bash \
#          \n rstudio-server stop' \
#          > /etc/services.d/rstudio/finish \
#    && mkdir -p /home/rstudio/.rstudio/monitored/user-settings \
#    && echo 'alwaysSaveHistory="0" \
#          \nloadRData="0" \
#          \nsaveAction="0"' \
#          > /home/rstudio/.rstudio/monitored/user-settings/user-settings \
#    && chown -R rstudio:rstudio /home/rstudio/.rstudio
#
#COPY envhack.sh /
#RUN bash /envhack.sh

# install of r-cran-foreign up above installs python2.7 as a dependency, so it
# busts our python3 symlink. some bullshit
RUN rm /usr/bin/python \
    && ln -s /usr/bin/python3 /usr/bin/python

EXPOSE 8787

COPY starthack.sh /
RUN chmod +x /starthack.sh

CMD ["/starthack.sh"]
