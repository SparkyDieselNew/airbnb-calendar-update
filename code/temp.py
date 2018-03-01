"""
    1. Download / read booking information from airbnb
    2. Set cleaning dates in two hours sessions based on the downloaded info
    3. Add the cleaning dates into a custom google calendar

    pip install --upgrade google-api-python-client
    pip install ics

    Google Calendar API auth based on this: https://developers.google.com/google-apps/calendar/quickstart/python

"""
from __future__ import print_function

import httplib2
import os
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from ics import Calendar




#url = 'https://drive.google.com/uc?export=download&id=0BwifSvR05dAOUzdaR1BtRVg0MG8'
url = 'https://www.airbnb.com/calendar/ical/3592620.ics?s=fec26381fe1e4c744fc7374e36ac9554'
#url = 'https://calendar.google.com/calendar/ical/8gva4r4arn89arfh210j0kldtc%40group.calendar.google.com/private-d276e0cf404c8c59649b8b47568467a8/basic.ics'
#wget.download(url)
#os.system('wget -O airbnb_cal.ics ' + url)
my_ics_file = open('airbnb_cal.ics', 'r')
my_calendar = Calendar(my_ics_file.read())
#print(my_calendar.events)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'AirBnB CalConnect'


def get_credentials():
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

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def list_calendars():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    calendar_list = service.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
       print(calendar_list_entry['summary'] + ' === ' + calendar_list_entry['id'])

    # calendar_dict = dict(list(enumerate(calendar_list['items'])))
    # print(calendar_dict[0])
    # print(calendar_list['items'][0]['id'])


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """


    event = {
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2018-01-01T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2015-05-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    event = service.events().insert(calendarId='vq2iggnttu8nv3ehmon7bjfjhk@group.calendar.google.com', body=event).execute()

"""
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
"""

if __name__ == '__main__':
    main()
