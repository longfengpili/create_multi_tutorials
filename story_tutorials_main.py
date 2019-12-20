'''
@Author: longfengpili
@Date: 2019-11-13 16:04:28
@LastEditTime : 2019-12-20 16:24:08
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from mysetting import *
from excel_api import WriteDataToExcel
from excel_api import File
from tutorials import StoryTutorial
import os
import time
from datetime import datetime


def get_datas(storytutorial_file, game_version):
    s_tutorial = StoryTutorial(storytutorial_file, game_version)
    datas = s_tutorial.get_datas_from_file()
    datas = s_tutorial.combin_story_funnel(datas)
    return datas

def write_data_to_excel(tutorial_output_path, datas):
    write_data_to_excel = WriteDataToExcel(tutorial_output_path)
    write_data_to_excel.write_sheets(datas)
    for sheetname in datas:
        write_data_to_excel.set_sheet_formula_conditional(sheetname, 'A1:F10000', '=AND($F1="end", LEN($C1) < 8)')
        write_data_to_excel.write_cell(sheetname, "G1", 'is_check')
        write_data_to_excel.set_sheet_formula_conditional(sheetname, 'A1:F10000', '=$G1=1', bg_color='#00b8ff')
    write_data_to_excel.close()


def story_write_main(storytutorial_file, game_version, tutorial_output_path='./output'):
    filename = datetime.now().strftime('%Y%m%d')
    tutorial_output_path = os.path.join(tutorial_output_path, f'{filename}storytutorial.xlsx')
    file = File(tutorial_output_path)
    file.close_file()
    time.sleep(2)
    datas = get_datas(storytutorial_file, game_version)
    write_data_to_excel(tutorial_output_path, datas)
    file.open_file()

if __name__ == '__main__':
    story_write_main(storytutorial_file, game_version)
