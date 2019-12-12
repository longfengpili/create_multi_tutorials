'''
@Author: longfengpili
@Date: 2019-12-12 11:03:01
@LastEditTime: 2019-12-12 12:16:25
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from excel_api import ReadDataFromExcel
from mysetting import *

class StoryTutorial(object):
    
    def __init__(self, storytutorial_file):
        self.storytutorial_file = storytutorial_file
        self.sheetname = 'StoryDialogStep'
        self.columns = ['id', 'Questid', 'BI']

    def get_datas_from_file(self):
        r_excel = ReadDataFromExcel(self.storytutorial_file)
        datas = r_excel.get_sheet_values_by_columns(self.sheetname, self.columns, header_row=2)
        datas = list(filter(lambda data: sum(map(lambda elem: isinstance(elem, str) if elem else 0, data)) == 0, datas)) #过滤掉有字符串的row
        datas = list(map(lambda data: list(map(lambda elem: int(elem) if elem else 0, data)), datas)) #全部转换成int
        return datas

    def combin_story_funnel(self, datas):
        id = 1
        current_questid = None
        story_funnel = []
        for data in datas:
            pass







    
