# -*- coding: utf-8 -*-
from oauth2client import file, client, tools
from httplib2 import Http
from apiclient.discovery import build

# TODO: argument parsing
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class GoogleCal:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.store = file.Storage('storage.json')
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets('client_secret.json', self.scopes)
            self.creds = tools.run_flow(self.flow, self.store, flags) if flags else tools.run(self.flow, self.store)

    def build_calendar(self):
        self.calendar = build('calendar', 'v3', http=self.creds.authorize(Http()))
        return self.calendar

    def insert_event(self, event):
        return self.calendar.events().insert(calendarId='primary', body=event).execute()
