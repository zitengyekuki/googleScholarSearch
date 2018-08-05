#coding: utf-8
#!/usr/bin/python


from selenium import webdriver
import time
import xlrd
import xlwt
from xlutils.copy import copy

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
        get_info(last_name, first_name)
        time.sleep(10)


def get_info(last_name, first_name):
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    name = last_name + '+' + first_name
    url = 'https://x.zhoupen.cn/scholar?hl=zh-CN&as_sdt=0%2C5&q='+name+''
    print url
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
    except:
        print 'continue'
    try:
        profile = driver.find_element_by_xpath('//*[@id="gs_res_ccl_mid"]/div[1]/table')
        if len(profile.find_elements_by_tag_name('div')) > 2:
            try:
                cited_number = profile.find_elements_by_tag_name('div')[2].text.split(u'：')[1]
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
    except:
        workbook = xlrd.open_workbook(NO_RESULT_FILE_NAME)
        sheet = workbook.sheet_by_index(0)
        rowNum = sheet.nrows
        newbook = copy(workbook)
        newsheet = newbook.get_sheet(0)
        newsheet.write(rowNum, 0, last_name)
        newsheet.write(rowNum, 1, first_name)
        newbook.save(NO_RESULT_FILE_NAME)
    driver.close()


if __name__ == '__main__':
    read('data.xls')
