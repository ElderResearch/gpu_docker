#!/usr/bin/env python3

import argparse
import docker
import json
import logging
import os
import os.path as op
import sys
import time

from docker import APIClient
from logging.handlers import RotatingFileHandler

_base_dir = op.dirname(op.abspath(__file__))
_log_dir = '/var/log/gpu_docker'

logger = logging.getLogger('gpu_docker')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

if not op.exists(_log_dir) or not os.access(_log_dir, os.W_OK):
    msg = 'Error accessing log directory. Logging to {}'
    logger.debug(msg.format(op.join(_base_dir, 'logs', 'build.log')))
    if not op.exists('logs'):
        os.mkdir('logs')
    _log_dir = op.join(_base_dir, 'logs')

file_handler = RotatingFileHandler(op.join(_log_dir, 'build.log'), delay=True,
                                   backupCount=10, encoding='utf-8')
file_handler.doRollover()
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(file_handler)

# do not rearrange these!
build_order = ['eri_python', 'eri_dev', 'eri_python_r', 'eri_dev_p_r']

def main(build_dict):
    logger.info('BUILD STARTED BY %s\n', os.getenv('USER', 'unknown'))
    cli = APIClient(base_url='unix://var/run/docker.sock')
    dry_run = build_dict.pop('dry_run')
    build_dict.update(
        {
            'rm': True,
            'labels': {
                'builder': os.getenv('USER'),
                'build_time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            }
        }
    )
    for image in build_order:
        d = build_dict.copy()
        d['tag'] = image + ':' + build_dict['tag']
        d['path'] = op.join(_base_dir, image)
        if dry_run:
            logger.info('DRY RUN: Building image %s', d['tag'])
        else:
            try:
                build_stream = cli.build(**d)
                for line in build_stream:
                    msg = '{}: {}'.format(image, json.loads(line).get('stream', ''))
                    logger.info(msg)
            except Exception as e:
                logger.error(e, exc_info=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GPU Docker Build Script")

    parser.add_argument(
        '-t', '--tag', metavar='XXXX', default='latest',
        help='A tag to add to the final images (default: %(default)s)'
    )

    parser.add_argument(
        '--no-cache', action='store_true', default=False, dest='nocache',
        help='Don’t use the cache when set to True (default: %(default)s)'
    )

    parser.add_argument(
        '--dry-run', action='store_true', default=False,
        help='Print messages but don\'t build images. (default: %(default)s)'
    )

    args = vars(parser.parse_args())
    main(args)
