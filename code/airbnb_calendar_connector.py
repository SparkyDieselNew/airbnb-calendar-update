from __future__ import print_function
import httplib2
import os
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from ics import Calendar


class GoogleCalendarConnector:
    #def __init__(self):
        

    def get_credentials(self):

        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'AirBnB CalConnect'

        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        home_dir = os.path.dirname(os.path.realpath(__file__))

        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        _credentials = store.get()
        if not _credentials or _credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                _credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                _credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return _credentials

    def connect(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

    def list_calendars(self, p_service):
        calendar_list = p_service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
           print(calendar_list_entry['summary'] + ' === ' + calendar_list_entry['id'])

    def add_event(self, p_service):
        event = {
          'summary': 'Takarítás',
          'location': 'W66 / Szilágyi',
          'description': 'Generated 6 digit code',
          'start': {
            'dateTime': '2018-01-01T09:00:00',
            'timeZone': 'Europe/Zurich',
          },
          'end': {
            'dateTime': '2018-01-01T17:00:00',
            'timeZone': 'Europe/Zurich',
          }
        }
        event = p_service.events().insert(calendarId='vq2iggnttu8nv3ehmon7bjfjhk@group.calendar.google.com', body=event).execute()


"""
    --- AirbnbCalendarConnector ---
    Class to connect to the Airbnb calender and download the ics file.
"""


class AirbnbCalendarConnector:
    #def __init__(self):
    #    return __name__

    def download_ics(self, calendar_url, calendar_filename):
        try:
            os.system('wget -O ' + calendar_filename + ' ' + calendar_url)
            return True
        except:
            return False

    def import_ics(self, calendar_filename):
        try:
            my_ics_file = open(calendar_filename, 'r')
            return Calendar(my_ics_file.read())
        except Exception as e:
            raise e
