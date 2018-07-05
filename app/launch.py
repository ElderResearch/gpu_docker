#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: launch.py
Author: eri
Created: 2018-05-25

Description:
    script for launching eri gpu containers

Usage:
    <usage>

"""

import argparse
import copy
import datetime
import collections
import hashlib
import logging
import os
import pwd

import dateutil.parser
import docker
import notebook.auth
import psutil
import pytz


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))

GPU_DEV = 'gpu_dev'
GPU_PROD = 'gpu_prod'
GPU_DEV_W_R = 'gpu_dev_w_r'
GPU_PROD_W_R = 'gpu_prod_w_r'
NO_GPU_DEV = 'no_gpu_dev'
ERI_IMAGES = {
    GPU_DEV: {
        'image': 'eri_dev:latest',
        'auto_remove': True,
        'detach': True,
        'ports': {8888: 8889},
        'NV_GPU': '0',
    },
    GPU_PROD: {
        'image': 'eri_prod:latest',
        'auto_remove': True,
        'detach': True,
        'ports': {8888: 8888},
        'NV_GPU': '1',
    },
    GPU_DEV_W_R: {
        'image': 'eri_dev_p_r:latest',
        'auto_remove': True,
        'detach': True,
        'ports': {8888: 8889, 8787: 8788},
        'NV_GPU': '0',
    },
    GPU_PROD_W_R: {
        'image': 'eri_prod_p_r:latest',
        'auto_remove': True,
        'detach': True,
        'ports': {8888: 8888, 8787: 8787},
        'NV_GPU': '1',
    },
    NO_GPU_DEV: {
        'image': 'eri_nogpu_dev:latest',
        'auto_remove': True,
        'detach': True,
        'ports': {8888: 'auto'},
    },
}
GPU_IMAGES = [k for (k, v) in ERI_IMAGES.items() if 'NV_GPU' in v]
JUPYTER_IMAGES = [
    k for (k, v) in ERI_IMAGES.items() if 8888 in v.get('ports', {})
]
R_IMAGES = [k for (k, v) in ERI_IMAGES.items() if 8787 in v.get('ports', {})]
SUCCESS = 'success'
FAILURE = 'failure'

LOGGER = logging.getLogger('launch')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def _error(msg):
    return {
        'error': True,
        'message': msg,
        'status': FAILURE,
    }


def _image_lookup(k, v):
    """iterate through ERI_IMAGES and return the internal tag and dictionary
    for the first item that contains key k with value v

    """
    for imagetag, imagedict in ERI_IMAGES.items():
        if k in imagedict and imagedict[k] == v:
            return imagetag, imagedict

    return None, None


def _running_images(client=None, ignore_other_images=False):
    return [tag for c in client.containers.list() for tag in c.image.tags]


def _env_lookup(c, key):
    """try and pull out the environment variable within container c"""
    try:
        for entry in c.attrs['Config']['Env']:
            i = entry.find('=')
            k = entry[:i]
            v = entry[i + 1:]
            if k == key:
                return v
    except:
        return None


def active_eri_images(client=None, ignore_other_images=False):
    client = client or docker.from_env()
    active = []

    for c in client.containers.list():
        try:
            image = c.attrs['Config']['Image']
        except Exception as e:
            print('untagged image {}'.format(c.image.id))
            continue

        # handle the untagged "latest" images:
        if len(image.split(':')) < 2:
            image = '{}:latest'.format(image)

        imagetype, imagedict = _image_lookup('image', image)

        if ignore_other_images and (imagetype is None):
            continue

        d = {
            'image': image,
            'imagetype': imagetype,
            'id': c.id,
        }

        if imagetype in JUPYTER_IMAGES + R_IMAGES:
            # we set a password value to launch this image; go get it
            pw = _env_lookup(c, 'PASSWORD')
            d['pwhash'] = hashlib.md5(pw.encode()).hexdigest()

        if imagetype in JUPYTER_IMAGES:
            # go get the actual mapped port (dynamically allocated for non-gpu
            # dev boxes, so can't just pull it from the imagedict in ERI_IMAGES
            # which we looked up a few lines back)
            port = int(
                c.attrs['HostConfig']['PortBindings']['8888/tcp'][0]['HostPort']
            )

            d['jupyter_url'] = 'http://eri-gpu:{}'.format(port)

        if imagetype in R_IMAGES:
            # similarly for the rstudio server, go find the port from the
            # container config
            port = int(
                c.attrs['HostConfig']['PortBindings']['8787/tcp'][0]['HostPort']
            )

            d['rstudio_url'] = 'http://eri-gpu:{}'.format(port)

        # check for a username environment variable
        d['username'] = _env_lookup(c, 'USER')

        # uptime
        try:
            t0 = dateutil.parser.parse(c.attrs['Created']).astimezone()
            t1 = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
            d['uptime'] = str(t1 - t0)
        except Exception as e:
            d['uptime'] = str(e)

        active.append(d)

    return active


def _validate_launch(imagetype=GPU_DEV, client=None):
    """basically, keep gpu instances unique

    args:
        imagetype (str): module-specific enumeration of available images
            (default: 'gpu_dev', which points to docker image `eri_dev:latest`)
        client (docker.client.DockerClient): the docker client object
            (default: None, which builds the basic client using
            `docker.from_env`)

    returns:
        bool: whether or not it is ok to launch a container of type `imagetype`

    raises:
        None

    """
    client = client or docker.from_env()
    if imagetype in [GPU_DEV, GPU_PROD]:
        if ERI_IMAGES[imagetype] in _running_images(client):
            return (
                False,
                "only one instance of {} allowed at a time".format(imagetype)
            )
        else:
            return True, None
    elif imagetype in ERI_IMAGES:
        return True, None

    # not defined
    return False, "imagetype {} not handled yet".format(imagetype)


def _update_environment(imagedict, key, val):
    """update the environment variable param in imagedict

    the imagedict dictionary doesn't necessarily have an environment key and
    value on launch, *and furthermore* this is complicated by the fact that
    the value for environment could be a list or a dictionary, so we have to do
    some bullshit

    """
    env = imagedict.get('environment', {})
    if isinstance(env, dict):
        env[key] = val
    else:
        env.append('{}={}'.format(key, val))
    imagedict['environment'] = env


def _setup_jupyter_password(imagedict, jupyter_pwd=None):
    if jupyter_pwd is None:
        msg = "you must provide a password for the jupyter notebook service"
        return False, _error(msg)

    # the neighboring jupyter_notebook_config.py file will look for an
    # environment variable PASSWORD, so we need to set that in our container
    _update_environment(imagedict, 'PASSWORD', jupyter_pwd)

    return True, None


def _find_open_port(start=8890, stop=9000):
    used_ports = {
        connection.laddr.port
        for connection in psutil.net_connections()
    }

    for port in range(start, stop + 1):
        if port not in used_ports:
            return port, None

    return (
        False,
        "unable to allocate open port between {} and {}".format(start, stop)
    )


def launch(username, imagetype=GPU_DEV, jupyter_pwd=None, **kwargs):
    """launch a docker container for user `username` of type `imagetype`

    args:
        username (str): linux user name, used for mounting home directories
        imagetype (str): module-specific enumeration of available images
            (default: 'gpu_dev', which points to docker image `eri_dev:latest`)
        jupyter_pwd (str): password for jupyter notebook signin
        kwargs (dict): all other keyword args are passed to the
            `client.containers.run` function

    returns:
        dict: json-able response string declaring the launched contianer id and
            possibly other important information, or an error message if
            launching failed for some reason

    raises:
        None

    """
    # is this image type defined (could just check image names directly...)
    try:
        imagedict = copy.deepcopy(ERI_IMAGES[imagetype])
    except KeyError:
        return _error("image type '{}' is not defined".format(imagetype))

    # check to see if launching the provided image is allowed
    client = docker.from_env()
    launchable, msg = _validate_launch(imagetype, client)
    if not launchable:
        return _error(msg)

    # check for user name and add that as the `user` value if it exists
    try:
        p = pwd.getpwnam(username)
        imagedict['user'] = '{p.pw_uid}:{p.pw_gid}'.format(p=p)

        # add the user's name as an environment variable. for shits and gigs,
        # but also because it helps us build our webapp down the line
        _update_environment(imagedict, 'USER', username)
    except KeyError:
        msg = "user '{}' does not exist on this system; contact administrators"
        msg = msg.format(username)
        return _error(msg)
    except Exception as e:
        return _error("unhandled error getting user name info: {}".format(e))

    # verify that this user has a home directory on the base server (will be
    # used in mounting step)
    user_home = os.path.expanduser('~{}'.format(username))
    if not os.path.isdir(user_home):
        # should have been done as part of account creation, error
        msg = "user '{}' does not have a home directory; contact administrators"
        msg = msg.format(username)
        return _error(msg)
    else:
        # it does exist, so we will mount it below in the `volumes` block.
        # expose it as a HOME variable in the image itself
        _update_environment(imagedict, 'HOME', user_home)

    # take care of some of the jupyter notebook specific steps
    if imagetype in JUPYTER_IMAGES:
        # configure the jupyter notebook password
        success, msg = _setup_jupyter_password(imagedict, jupyter_pwd)
        if not success:
            return _error(msg)

        # update ports dictionary for this instance if this is an auto
        if imagedict['ports'][8888] == 'auto':
            # have to find the first port over 8889 that is open
            port, msg = _find_open_port(start=8890, stop=9000)
            if not port:
                return _error(msg)

            imagedict['ports'][8888] = port

    # launch container based on provided image, mounting notebook directory from
    # user's home directoy
    volumes = {
        'volumes': {
            user_home: {'bind': user_home, 'mode': 'rw'},
            '/etc/group': {'bind': '/etc/group', 'mode': 'ro'},
            '/etc/passwd': {'bind': '/etc/passwd', 'mode': 'ro'},
            '/etc/skel': {'bind': '/etc/skel', 'mode': 'ro'},
            '/data': {'bind': '/data', 'mode': 'rw'},
        }
    }

    # if the NV_GPU environment variable was passed in via imagedict, set the
    # proper runtime value and add an environment variable flag
    if imagetype in GPU_IMAGES:
        imagedict['runtime'] = 'nvidia'
        _update_environment(
            imagedict,
            'NVIDIA_VISIBLE_DEVICES',
            imagedict.pop('NV_GPU')
        )
    else:
        _update_environment(
            imagedict,
            'NVIDIA_VISIBLE_DEVICES',
            'none'
        )

    try:
        # look upon my kwargs hack and tremble. later dicts have priority
        container = client.containers.run(**{**imagedict, **volumes, **kwargs})
    except Exception as e:
        return _error("error launching container: '{}'".format(e))

    d = {
        'message': 'container launched successfully',
        'status': SUCCESS,
        'imagetype': imagetype,
        'jupyter_url': 'http://eri-gpu:{}/'.format(imagedict['ports'][8888]),
        'image': imagedict['image'],
    }

    if imagetype in R_IMAGES:
        d['rstudio_url'] = 'http://eri-gpu:{}'.format(imagedict['ports'][8787])

    for attr in ['id', 'name', 'status']:
        d[attr] = getattr(container, attr)

    return d


def kill(docker_id):
    try:
        docker.from_env().containers.get(docker_id).kill()
        d = {
            'message': 'container killed successfully',
            'status': SUCCESS,
        }
    except Exception as e:
        d = _error("unable to kill docker container")
        d['error_details'] = str(e)

    d['docker_id'] = docker_id

    return d


# ----------------------------- #
#   Command line                #
# ----------------------------- #

def parse_args():
    parser = argparse.ArgumentParser()

    username = "user name (must be a created user on the gpu box)"
    parser.add_argument("-u", "--username", help=username)

    imagetype = "type of image to launch"
    parser.add_argument(
        "-t", "--imagetype", help=imagetype, choices=ERI_IMAGES.keys(),
        default=GPU_DEV
    )

    jupyter_pwd = (
        "jupyter password (only required for environments which have jupyter"
        " notebook services running in them)"
    )
    parser.add_argument("-p", "--jupyterpwd", help=jupyter_pwd)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    launch(
        username=args.username,
        imagetype=args.imagetype,
        jupyter_pwd=args.jupyterpwd
    )
