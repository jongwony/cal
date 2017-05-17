# -*- coding: utf-8 -*-

import os
from inputconfig import Triming

current_dir = os.path.realpath(os.path.dirname(__file__))

# virtualenv
try:
    from googleoauth import GoogleCal
except ImportError:
    venv_name = '_ccal'
    osdir = 'Scripts' if os.name is 'nt' else 'bin'
    venv = os.path.join(venv_name, osdir, 'activate_this.py')
    activate_this = (os.path.join(current_dir, venv))
    # Python 3: exec(open(...).read()), Python 2: execfile(...)
    exec(open(activate_this).read(), dict(__file__=activate_this))
    
    from googleoauth import GoogleCal



DATE = input('날짜: ')
assert DATE is not '', '날짜가 없습니다.'
SUMMARY = input('제목: ')
assert SUMMARY is not '', '제목이 없습니다.'
LOCATION = input('위치: ')
DESCRIPTION = input('세부정보: ')
DURATION_H = input('기간(시간): ')
DURATION_D = input('기간(일): ')
ALARM = input('알람: ')

config = Triming(DATE, SUMMARY, LOCATION, DESCRIPTION, DURATION_H, DURATION_D, ALARM)
session = GoogleCal(current_dir)
session.build_calendar()

event = {
  'summary': config.summary,
  'location': config.location,
  'description': config.description,
  'start': {
    'dateTime': config.start_date(),
    'timeZone': 'Asia/Seoul',
  },
  'end': {
    'dateTime': config.end_date(),
    'timeZone': 'Asia/Seoul',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=' + config.duration_d
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
