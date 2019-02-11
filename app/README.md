# gpu launcher application

the launcher application is a `flask` webapp (defined in `launchapp.py`) which uses the `launch.py` library and the `docker` `python` package to launch `docker` containers and provide users urls to `jupyter notebook` or `rstudio` endpoints

the neighboring `launch.py` file could be used directly from the command line (e.g. to launch a single container). try `python launch.py --help` to see the options. that being said, you usually won't do that -- just use the webapp!

## the webapp

the way I have run this in the past is as follows (talk to andrew stewart to see if he has done something more robust since I last looked at it)

1. create a [`screen`](https://linuxize.com/post/how-to-use-linux-screen/) (full `man` page [here](https://linux.die.net/man/1/screen)) for a persistent terminal session
   1. you may want to give it an alias; you can do this with `screen -S alias` (e.g. `screen -S launchapp`)
1. within that `screen` session, make sure you have the bare bones environment built
   1. see `requirements.txt` for the list of packages. install those packages however you want
1. launch the app with `python launchapp.py`
1. leave the screen with the keyboard command sequence `Ctrl + a, d`

in the future, if you need to re-connect to the screen to check on the app itself, you can do so with `screen -r [id|alias`. you will have to provide the screen id number or the screen alias; both can be seen from `screen -list`

### killing

if you need to kill someone else's running `screen` process, search for it via

```sh
ps -aef | grep launchapp
```

or

```sh
ps -aef | grep flask
```

(depending on how it was launched), and kill that process. then, create your own `screen` and start the app
