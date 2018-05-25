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

import logging
import os
import pwd

import docker
import notebook.auth


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))

GPU_DEV = 'gpu_dev'
GPU_PROD = 'gpu_prod'
ERI_IMAGES = {
    GPU_DEV: {
        'image': 'eri_dev:latest',
        'auto_remove': True,
        'detach': True,
        'ports': {8888: 8889},
    },
    GPU_PROD: {
        'image': 'eri_prod:latest',
        'auto_remove': True,
        'detach': True,
        'ports': {8888: 8888},
    },
}
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


def _running_images(client=None):
    client = client or docker.from_env()
    return [tag for c in client.containers.list() for tag in c.image.tags]


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

    # not defined
    return False, "imagetype {} not handled yet".format(imagetype)


def _setup_jupyter_password(imagedict, jupyter_pwd=None):
    if jupyter_pwd is None:
        msg = "you must provide a password for the jupyter notebook service"
        return False, _error(msg)

    # the neighboring jupyter_notebook_config.py file will look for an
    # environment variable PASSWORD, so we need to set that in our container
    # this is complicated by the fact that environment could be a list or a
    # dictionary, so we have to do some bullshit
    env = imagedict.get('environment', {})
    if isinstance(env, dict):
        env['PASSWORD'] = jupyter_pwd
    else:
        env.append('PASSWORD={}'.format(jupyter_pwd))
    imagedict['environment'] = env

    return True, None


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
        imagedict = ERI_IMAGES[imagetype]
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
        print(imagedict['user'])
    except KeyError:
        msg = "user '{}' does not exist on this system; contact administrators"
        msg = msg.format(username)
        return _error(msg)

    # create notebook directory if it doesn't exist
    user_home = os.path.expanduser('~{}'.format(username))
    if not os.path.isdir(user_home):
        # should have been done as part of account creation, error
        msg = "user '{}' does not have a home directory; contact administrators"
        msg = msg.format(username)
        return _error(msg)

    # configure the jupyter notebook password if needed
    if imagetype in [GPU_DEV, GPU_PROD]:
        success, msg = _setup_jupyter_password(imagedict, jupyter_pwd)
        if not success:
            return _error(msg)

    # launch container based on provided image, mounting notebook directory from
    # user's home directoy
    volumes = {
        'volumes': {
            user_home: {'bind': '/userhome', 'mode': 'rw'},
            '/etc/group': {'bind': '/etc/group', 'mode': 'ro'},
            '/etc/password': {'bind': '/etc/password', 'mode': 'ro'},
        }
    }
    # look upon my kwargs hack and tremble. later dicts have priority
    container = client.containers.run(**{**imagedict, **volumes, **kwargs})

    d = {
        'message': 'container launched successfully',
        'status': SUCCESS,
    }

    for attr in ['id', 'name', 'status']:
        d[attr] = getattr(container, attr)

    # get jupyter notebook url if applicable

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
        jupyter_pwd=args.jupyter_pwd
    )
