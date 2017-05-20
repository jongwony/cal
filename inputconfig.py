# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
from collections import OrderedDict

def date_triming(date):
    """{'year':int, 'month':int, 'day':int, 'hour':int, 'minute':int, 'locale':string}"""
    trim_date = OrderedDict()

    # Today
    now = datetime.today()

    # parse criteria
    noon_criteria = {'오전': 'AM', '오후': 'PM'}
    nearday = {'오늘': 0, '내일': 1, '모레': 2}

    # ex) 내일 오후 3시 = 2017년 5월 17일 3시 0분 PM
    trim_date['year'] = str(now.year)

    month = re.findall(r'(\d+)월', date)
    assert len(month) <= 1, 'duplicate 월'
    trim_date['month'] = format(month[0]) if month else format(now.month)

    day = re.findall(r'(\d+)일', date)
    assert len(day) <= 1, 'duplicate 일'
    trim_date['day'] = format(day[0]) if day else format(now.day)

    # default time 7AM
    hour = re.findall(r'(\d+)시', date)
    assert len(hour) <= 1, 'duplicate 시'
    trim_date['hour'] = format(hour[0]) if hour else '7'

    minute = re.findall(r'(\d+)분', date)
    assert len(hour) <= 1, 'duplicate 분'
    trim_date['minute'] = format(minute[0]) if minute else '0'

    locale = re.findall(r'(오전|오후|AM|PM)', date)
    assert len(locale) <= 1, 'duplicate locale'
    trim_date['locale'] = noon_criteria[locale[0]] if locale else 'AM'

    # make datetime
    start_date = datetime.strptime('/'.join(trim_date.values()), '/'.join(['%Y', '%m', '%d', '%I', '%M', '%p']))

    near = re.findall(r'(오늘|내일|모레)', date)
    assert len(near) <= 1, 'duplicate near date'
    near_days = int(nearday[near[0]]) if near else 0
    near_delta = timedelta(days=near_days)

    return start_date + near_delta

class Configdata:
    def __init__(self):
        self.date = ''
        self.summary = ''
        self.location = ''
        self.description = ''
        self.h_duration = ''
        self.d_duration = ''
        self.alarm = ''

    def diary_triming(self, *args):
        self.date, self.summary, self.description = args
        self.description = '스크립트에 의해 자동 생성된 이벤트입니다.' if self.description is '' else self.description
        self.date = date_triming(self.date)

    def triming(self, *args):
        self.date, self.summary, self.description, self.location, self.duration_h, self.duration_d, self.alarm = args
        self.alarm = 10 if self.alarm is '' else int(self.alarm)
        self.duration_h = 1 if self.duration_h is '' else int(self.duration_h)
        self.duration_d = '1' if self.duration_d is '' else self.duration_d
        self.description = '스크립트에 의해 자동 생성된 이벤트입니다.' if self.description is '' else self.description
        self.date = date_triming(self.date)



    @property
    def date_linkform(self):
        return '%Y%m%dT%H%M00'

    @property
    def date_eventform(self):
        return '%Y-%m-%dT%H:%M:00'

    def start_date_format(self, form):
        return datetime.strftime(self.date, form)

    def end_date_format(self, form):
        end_date = self.date + timedelta(hours=self.duration_h)
        return datetime.strftime(end_date, form)
