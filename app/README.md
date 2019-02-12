# gpu launcher application

the launcher application is a `flask` webapp (defined in `launchapp.py`) which uses the `launch.py` library and the `docker` `python` package to launch `docker` containers and provide users urls to `jupyter notebook` or `rstudio` endpoints

the neighboring `launch.py` file could be used directly from the command line (e.g. to launch a single container). try `python launch.py --help` to see the options. that being said, you usually won't do that -- just use the webapp!

## the webapp

the launcher application is now served by apache and lives in the `/var/www` directory.
after committing/merging changes to the master branch on Github, you will have to pull those changes to the deployment directory and restart the apache service.

1. ssh into the gpu machine.
2. `cd /var/www/gpu_docker`
3. `git pull`
4. `sudo service apache2 restart`

the relevant apache2 virtual host config lives at `/etc/apache2/sites-enabled/gpu_docker.conf`

you can view the error log by running `sudo less /var/log/apache2/error.log`

CAUTION: other than running `git pull`, you should never directly edit the files located in `/var/www/gpu_docker`!
