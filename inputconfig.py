# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
from collections import OrderedDict

def query_trim(patch, query, els):
    refine = re.findall(patch, query)
    assert len(refine) <= 1, 'duplicate' + patch
    return refine[0] if refine else els

def date_triming(date):
    """{'year':int, 'month':int, 'day':int, 'hour':int, 'minute':int, 'locale':string}"""
    trim_date = OrderedDict()

    # Today
    now = datetime.today()

    # parse criteria
    noon_criteria = {'오전': 'AM', '오후': 'PM', 'AM': 'AM', 'PM': 'PM'}
    nearday = {'어제': -1, '오늘': 0, '내일': 1, '모레': 2}

    # ex) 내일 오후 3시 = 2017년 5월 17일 3시 0분 PM
    trim_date['year'] = format(query_trim(r'(\d+)년', date, now.year))
    trim_date['month'] = format(query_trim(r'(\d+)월', date, now.month))
    trim_date['day'] = format(query_trim(r'(\d+)일', date, now.day))

    # default time 7:00 AM
    trim_date['hour'] = format(query_trim(r'(\d+)시', date, 7))
    trim_date['minute'] = format(query_trim(r'(\d+)분', date, 0))

    trim_date['locale'] = noon_criteria[query_trim(r'(오전|오후|AM|PM)', date, 'AM')]

    # make datetime
    start_date = datetime.strptime('/'.join(trim_date.values()), '/'.join(['%Y', '%m', '%d', '%I', '%M', '%p']))

    near_days = int(query_trim(r'(어제|오늘|내일|모레)', date, 0))
    near_delta = timedelta(days=near_days)

    return start_date + near_delta

def duration_datetime(date):
    day = int(query_trim(r'(\d+)일', date, 1)) - 1
    hour = query_trim(r'(\d+)시', date, 1)
    minute = query_trim(r'(\d+)분', date, 0)

    return timedelta(days=day, hours=hour, minutes=minute)

class Configdata:
    def __init__(self):
        self.date = ''
        self.summary = ''
        self.location = ''
        self.description = ''
        self.duration = ''
        self.alarm = ''

    def diary_triming(self, *args):
        self.date, self.summary, self.description, self.duration = args
        self.description = '스크립트에 의해 자동 생성된 이벤트입니다.' if self.description is '' else self.description
        self.date = date_triming(self.date)
        self.duration = duration_datetime(self.duration)

    def triming(self, *args):
        self.date, self.summary, self.description, self.location, self.duration, self.alarm = args
        self.alarm = 10 if self.alarm is '' else int(self.alarm)
        self.description = '스크립트에 의해 자동 생성된 이벤트입니다.' if self.description is '' else self.description
        self.date = date_triming(self.date)
        self.duration = duration_datetime(self.duration)

    @property
    def date_diaryform(self):
        return '%Y-%m-%d'

    @property
    def date_linkform(self):
        return '%Y%m%dT%H%M00'

    @property
    def date_eventform(self):
        return '%Y-%m-%dT%H:%M:00'

    def start_datetime_format(self, form):
        return datetime.strftime(self.date, form)

    def end_datetime_format(self, form):
        end_date = self.date + self.duration
        return datetime.strftime(end_date, form)
