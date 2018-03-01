"""
    1. Download / read booking information from airbnb
    2. Set cleaning dates in two hours sessions based on the downloaded info
    3. Add the cleaning dates into a custom google calendar

    pip install --upgrade google-api-python-client
    pip install ics

    Google Calendar API auth based on this: https://developers.google.com/google-apps/calendar/quickstart/python

"""

from airbnb_calendar_connector import AirbnbCalendarConnector,GoogleCalendarConnector


def main():
    AIRBNB_CAL_URL = 'https://www.airbnb.com/calendar/ical/3592620.ics?s=fec26381fe1e4c744fc7374e36ac9554'
    GOOGLE_CAL_ID = 'vq2iggnttu8nv3ehmon7bjfjhk@group.calendar.google.com'


    #if AirbnbCalendarConnector.download_ics(calendar_url=url,calendar_filename='airbnbcal.ics'):
    #    My_AirBnB_Calendar =AirbnbCalendarConnector.import_ics(calendar_filename='airbnbcal.ics')
    #    print(My_AirBnB_Calendar.events)

    My_Google_Calendar = GoogleCalendarConnector()
    Service = My_Google_Calendar.connect()
    My_Google_Calendar.list_calendars(Service)
    #My_Google_Calendar.add_event(Service)


if __name__ == '__main__':
    main()
