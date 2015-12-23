# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = '目覚マシマシ'

class Calendar:
    """docstring for Google Calender"""

    def __init__(self):
        self.credentials = self.get_credentials()
        self.events = []

    # まだ一つもcredentialsが作られていなかったら作成させられる。
    # だから一番最初にこの時計が起動させられた時に、scheduleを利用するかどうかきいて、利用するなら認証画面に飛んで行ってくれて、そこで自分のメールアドレス宛に認証を送る。でそれに同意すればscheduleが利用できるようになる。
    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        self.credentials = credentials
        return self

    def get_events(self, timeMin=False, timeMax=False, eventsMax=False):
        """
        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        http = self.credentialsauthorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        if not timeMin:
            timeMin = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        if not timeMax:
            timeMax = 0
        if not eventsMax:
            eventsMax = 10
        print('Getting the upcoming {0} events').format(eventsMax)
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

def main():

    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    cal = Calendar()
    credentials = cal.get_credentials().credentials
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        print(start, event['summary'])


if __name__ == '__main__':
    print('Python', python_version())
    main()
