#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import requests
import xlrd
import xlwt
from xlutils.copy import copy
from bs4 import BeautifulSoup


time_stamp = str(int(time.time()))
RESULT_FILE_NAME = 'result_'+time_stamp+'.xls'
NO_RESULT_FILE_NAME = 'noresult_'+time_stamp+'.xls'


def read(path):
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    excel_result = xlwt.Workbook(encoding='utf-8')
    excel_noresult = xlwt.Workbook(encoding='utf-8')
    excel_result_sheet1 = excel_result.add_sheet('Sheet 1')
    excel_result_sheet1.write(0, 0, 'LAST NAME')
    excel_result_sheet1.write(0, 1, 'FIRST NAME')
    excel_result_sheet1.write(0, 2, 'CITED')
    excel_noresult_sheet1 = excel_noresult.add_sheet('Sheet 1')
    excel_noresult_sheet1.write(0, 0, 'LAST NAME')
    excel_noresult_sheet1.write(0, 1, 'FIRST NAME')
    excel_result.save(RESULT_FILE_NAME)
    excel_noresult.save(NO_RESULT_FILE_NAME)

    for i in range(1, nrows):
        last_name = table.cell(i, 0).value
        first_name = table.cell(i, 1).value
        search(last_name, first_name)
        time.sleep(30)


def search(last_name, first_name):
    name = last_name + '+' + first_name
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + name + '&btnG='
    print url
    result = requests.get(url)
    if result.status_code == 200:
        c = result.content
        soup = BeautifulSoup(c, 'lxml')
        get_result(soup, last_name, first_name)
    else:
        print 'rest-----'
        time.sleep(300)
        search(last_name, first_name)


def get_result(soup, last_name, first_name):
    profile = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['gs_r'])
    if profile:
        if len(profile[0].find_all('div')) > 2:
            try:
                cited_number = profile[0].find_all('div')[2].text.split('Cited by ')[1]
            except:
                cited_number = '0 or multiple_person_need_check'
        else:
            cited_number = 'multiple_person_need_check'
        workbook = xlrd.open_workbook(RESULT_FILE_NAME)
        sheet = workbook.sheet_by_index(0)
        rowNum = sheet.nrows
        newbook = copy(workbook)
        newsheet = newbook.get_sheet(0)
        newsheet.write(rowNum, 0, last_name)
        newsheet.write(rowNum, 1, first_name)
        newsheet.write(rowNum, 2, cited_number)
        newbook.save(RESULT_FILE_NAME)
    else:
        workbook = xlrd.open_workbook(NO_RESULT_FILE_NAME)
        sheet = workbook.sheet_by_index(0)
        rowNum = sheet.nrows
        newbook = copy(workbook)
        newsheet = newbook.get_sheet(0)
        newsheet.write(rowNum, 0, last_name)
        newsheet.write(rowNum, 1, first_name)
        newbook.save(NO_RESULT_FILE_NAME)

if __name__ == '__main__':
    try:
        path = sys.argv[1]
        read(path)
    except Exception, e:
        print e
        print '[Error] invalid file path, for example: python search.py xxxx.xlsx'

