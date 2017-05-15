# -*- coding: utf-8 -*-
from inputconfig import Triming
from googleoauth import GoogleCal

DATE = input('날짜: ')
SUMMARY = input('제목: ')
LOCATION = input('위치: ')
DESCRIPTION = input('세부정보: ')
DURATION = input('기간: ')
ALARM = input('알람: ')

config = Triming(DATE, SUMMARY, LOCATION, DESCRIPTION, DURATION, ALARM)
session = GoogleCal()
session.build_calendar()

event = {
  'summary': config.date,
  'location': config.location,
  'description': config.description,
  'start': {
    'dateTime': config.start_date,
    'timeZone': 'Asia/Seoul',
  },
  'end': {
    'dateTime': config.end_date,
    'timeZone': 'Asia/Seoul',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
#   'attendees': [
#     {'email': 'lpage@example.com'},
#     {'email': 'sbrin@example.com'},
#   ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

print('Event created: {}'.format(session.insert_event(event).get('htmlLink')))
