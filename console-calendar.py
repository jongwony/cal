# -*- coding: utf-8 -*-
import venv
from inputconfig import Configdata
from googleoauth import GoogleCal
import argparse
import time
import os
import urllib

def push_event(config):
  session = GoogleCal(venv.SCRIPTDIR)
  session.build_calendar()

  event = {
    'summary': config.summary,
    'location': config.location,
    'description': config.description,
    'start': {
      'dateTime': config.start_date_format(config.date_eventform),
      'timeZone': 'Asia/Seoul',
    },
    'end': {
      'dateTime': config.end_date_format(config.date_eventform),
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
        {'method': 'popup', 'minutes': config.alarm},
      ],
    },
  }

  session.insert_event(event)

def make_ics(config):
  uid = time.strftime('%Y-%m-%d_%H%M%S')

  ics_format = """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
PRODID:Product by Jongwon
BEGIN:VEVENT
UID:{}
DTSTART:{}
DTEND:{}
LOCATION:{}
SUMMARY:{}
DESCRIPTION:{}
BEGIN: VALARM
TRIGGER: -PT{}M
DESCRIPTION:{}
END:VALARM
END:VEVENT
END:VCALLENDAR""".format(
    uid,
    config.start_date_format(config.date_linkform),
    config.end_date_format(config.date_linkform),
    config.location,
    config.summary,
    config.description,
    config.alarm,
    config.description
  )

  # binary encoding
  ics_format = ics_format.encode('utf-8')

  # make ics
  filename = uid + '.ics'
  abspath = os.path.join(venv.SCRIPTDIR, filename)
  with open(abspath, 'wb') as f:
      f.write(ics_format)

  #os.system('start ' + abspath)
  return abspath

def google_link(config):
  uri = 'http://www.google.com/calendar/event'
  param = {
    'action': 'TEMPLATE',
    'text': config.summary,
    'dates': '/'.join([
    config.start_date_format(config.date_linkform),
    config.end_date_format(config.date_linkform)
    ]),
    'details': config.description,
    'location': config.location,
  }

  link = uri + '?' + urllib.parse.urlencode(param)
  return link

def write_diary(config):
  session = GoogleCal(venv.SCRIPTDIR)
  session.build_calendar()

  event = {
    'summary': config.summary,
    'description': config.description,
    'start': {
      'dateTime': config.start_date_format(config.date_eventform),
      'timeZone': 'Asia/Seoul',
    },
    'end': {
      'dateTime': config.end_date_format(config.date_eventform),
      'timeZone': 'Asia/Seoul',
    }
  }
  session.insert_event(event)

def quick_init():
  query = input('Query: ')
  return query

def quick_add(query):
  session = GoogleCal(venv.SCRIPTDIR)
  session.build_calendar()
  session.quick_event(query)

def call_list():
  session = GoogleCal(venv.SCRIPTDIR)
  session.build_calendar()
  #session.calendar_list_all()
  session.calendar_lists()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', help='Make ics file', action='store_true')
  parser.add_argument('-d', help='Write diary', action='store_true')
  parser.add_argument('-g', help='Google calendar link', action='store_true')
  parser.add_argument('--no-push', help="Don't push my calendar", action='store_false')
  parser.add_argument('-q', help='Push quickAdd calendar', action='store_true')
  parser.add_argument('-l', help='Calendar lists', action='store_true')

  args = parser.parse_args()

  if args.l:
    call_list()
    quit()

  # Quick Add Calendar
  if args.q:
    query = quick_init()
    quick_add(query)
    print('Event created.')
    quit()

  # Initialize
  config = Configdata()

  date = input('날짜: ')
  assert date is not '', '날짜가 없습니다.'
  summary = input('제목: ')
  assert summary is not '', '제목이 없습니다.'
  description = input('세부정보: ')

  # Diary
  if args.d:
    config.diary_triming(date, summary, description)
    write_diary(config)
    print('Event created.')
    quit()

  location = input('위치: ')
  h_duration = input('기간(시간): ')
  d_duration = input('기간(일): ')
  alarm = input('알람(분 전): ')
  config.triming(date, summary, description, location, h_duration, d_duration, alarm)

  # ICS file
  if args.i:
    abspath = make_ics(config)
    print('ics file created at' + abspath)

  # Google Calendar link
  if args.g:
    link = google_link(config)
    print('google link: ' + link)
  
  if args.no_push:
    push_event(config)
    print('Event created.')
