from __future__ import print_function
import json
from logging import fatal
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from ScheduleReader import getShifts

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def main():

    f = open('CalendarIds.json', 'r')
    calendarIds = json.load(f)

    TEST_CALENDAR = calendarIds['test']
    WORK_CALENDAR = calendarIds['work']
    FAMILY_CALENDAR = calendarIds['family']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    shifts = getShifts()	

    for shift in shifts:
        #result = service.events().insert(calendarId=TEST_CALENDAR, body=shift.event).execute()
        service.events().insert(calendarId=WORK_CALENDAR, body=shift.event).execute()
        service.events().insert(calendarId=FAMILY_CALENDAR, body=shift.familyEvent).execute()

if __name__ == '__main__':
    main()