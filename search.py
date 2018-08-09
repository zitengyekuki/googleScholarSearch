#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import requests
from bs4 import BeautifulSoup


def search(name):
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + name + '&btnG='
    print url
    result = requests.get(url)
    if result.status_code == 200:
        c = result.content
        soup = BeautifulSoup(c, 'lxml')
        get_result(soup, name)
    else:
        print 'rest-----'
        time.sleep(10)
        search(name)


def get_result(soup, name):
    profile = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['gs_r'])
    if profile:
        if len(profile[0].find_all('div')) > 2:
            try:
                cited_number = profile[0].find_all('div')[2].text.split('Cited by ')[1]
            except:
                cited_number = '0 or multiple_person_need_check'
        else:
            cited_number = 'There are multiple person with this name, please check'
        print (name + ', cited_number:' + cited_number)
    else:
        print('no result')

if __name__ == '__main__':
    try:
        name = sys.argv[1]
        search(name)
    except Exception, e:
        print e
        print '[Error] invalid file path, for example: python search.py "FirstName+LastName"'

