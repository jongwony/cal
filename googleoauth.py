# -*- coding: utf-8 -*-
from oauth2client import file, client, tools
from httplib2 import Http
from apiclient.discovery import build
import os

class GoogleCal:
    def __init__(self, project_dir):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.store = file.Storage(os.path.join(project_dir, 'storage.json'))
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets(os.path.join(project_dir,'client_secret.json'), self.scopes)
            self.creds = tools.run(self.flow, self.store)

    def build_calendar(self):
        self.calendar = build('calendar', 'v3', http=self.creds.authorize(Http()))
        return self.calendar

    def insert_event(self, event):
        return self.calendar.events().insert(calendarId='primary', body=event).execute()

    def quick_event(self, query):
        return self.calendar.events().quickAdd(calendarId='primary',text=query).execute()

    def calendar_list_all(self):
        from datetime import datetime
        import re

        page_token = None
        while True:
            events = self.calendar.events().list(calendarId='primary', pageToken=page_token).execute()
            for event in events['items']:
                if event['status'] == 'confirmed':
                    date, = {'dateTime', 'date'}.intersection(set(event['start']))
                    date_trim = re.sub(r'(.*)T(\d+):(\d+)(.*)', r'\1 \2:\3', event['start'][date])
                    element = '{:<16} {} {}'.format(date_trim, event['summary'], event.get('reminders'))
                    print(element)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    def calendar_lists(self):
        from datetime import datetime
        from inputconfig import date_triming
        import re

        start = input('From: ')
        end = input('To: ')
        start_dt = date_triming(start)
        end_dt = date_triming(end)
        assert start_dt < end_dt, "Keep order!"

        items = list()
        page_token = None
        while True:
            events = self.calendar.events().list(calendarId='primary', pageToken=page_token).execute()
            for event in events['items']:
                if 'dateTime' in event['start']:
                    date = datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S+09:00')
                if 'date' in event['start']:
                    date = datetime.strptime(event['start']['date'], '%Y-%m-%d')
                items.append((date, EventItems(event)))
            page_token = events.get('nextPageToken')
            if not page_token:
                s = sorted(items, key=lambda t: t[0])
                for k, e in s:
                    if start_dt < k < end_dt:
                        print('{} {}'.format(datetime.strftime(k, '%Y-%m-%d %H:%M'), e.summary))
                break

class EventItems:
    def __init__(self, d):
        self.__dict__ = d
