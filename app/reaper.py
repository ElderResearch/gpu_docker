#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: reaper.py
Author: zlamberty
Created: 2018-07-05

Description:
    this kills the crab.

    had to install a bunch of shit. key install statement:
    pip install --user --upgrade pyOpenSSL

Usage:
    <usage>

"""

import argparse
import datetime
import logging
import logging.config
import os

import launch

from apiclient.discovery import build
from google.oauth2 import service_account
from httplib2 import Http
from oauth2client import file, client, tools


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

G_CAL_ID = 'datamininglab.com_6taegbbncqqjuv6pum1fo61ej8@group.calendar.google.com'
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

HERE = os.path.dirname(os.path.realpath(__file__))
LOGGER = logging.getLogger('reaper')


# ----------------------------- #
#   Main routine                #
# ----------------------------- #

def get_approved_sessions(google_calendar_id, f_cred):
    """check all running sessions against the official google calendar (GPU BOX)

    args:
        google_calendar_id (str): the google calendar id for the gpu box cal
        f_cred (str): file path to the credentials file used in the oauth step

    returns:
        list: list of summary dictionaries for sessions that were ICED

    raises:
        None

    """
    # Setup the Calendar API (manual user method)
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(f_cred, SCOPES)
        flags = argparse.Namespace(
            noauth_local_webserver=True, logging_level="INFO"
        )
        creds = tools.run_flow(flow, store, flags=flags)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # setup the calendar api (service account method)
    # I created a service account for this, it's defined, but it requires
    # domain-wide delegation of my user account to it and that is something I
    # cannot do on my own. see:
    # https://developers.google.com/api-client-library/php/auth/service-accounts
    #credentials = service_account.Credentials.from_service_account_file(
    #    f_cred, scopes=[SCOPE]
    #)
    #service = build('calendar', 'v3', credentials=credentials)

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(seconds=600)
    now = now.isoformat() + 'Z' # 'Z' indicates UTC time
    then = then.isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=google_calendar_id,
        timeMin=now,
        timeMax=then,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return [
        {
            'email': event['creator']['email'],
            'env': event['summary'].split()[0],
            'username': event['summary'].split()[1],
        }
        for event in events_result['items']
    ]


def reap(google_calendar_id, f_cred):
    """kill any currently running session that is not scheduled on the gcal

    this will be extremely aggressive by default

    args:
        google_calendar_id (str): the google calendar id for the gpu box cal
        f_cred (str): file path to the credentials file used in the oauth step

    returns:
        list: list of summary dictionaries for sessions that were ICED

    raises:
        None

    """
    approved_sessions = get_approved_sessions(google_calendar_id, f_cred)
    current_active_sessions = [
        session
        for session in launch.active_eri_images(ignore_other_images=True)
        if session['imagetype'] in launch.GPU_IMAGES
    ]

    for session in current_active_sessions:
        approved = False
        for approved_session in approved_sessions:
            if approved_session['username'] == session['username']:
                are_both_prod = (
                    approved_session['env'] == 'prod'
                    and session['imagetype'] in launch.PROD_IMAGES
                )
                are_both_dev = (
                    approved_session['env'] == 'dev'
                    and session['imagetype'] in launch.DEV_IMAGES
                )
                if are_both_prod or are_both_dev:
                    approved = True

        # if they aren't approved here, ICE
        if not approved:
            launch.kill(docker_id=session['id'])
            print('killed session: {}'.format(session))



# ----------------------------- #
#   Command line                #
# ----------------------------- #

def parse_args():
    """Take a log file from the commmand line"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--google_calendar_id', help='google calendar id',
        default=G_CAL_ID
    )

    parser.add_argument(
        '-f', '--f_cred', help="google calendar app credentials file"
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    reap(
        google_calendar_id=args.google_calendar_id,
        f_cred=args.f_cred
    )
