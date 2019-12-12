'''
@Author: longfengpili
@Date: 2019-11-13 16:04:28
@LastEditTime: 2019-12-12 14:05:42
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from mysetting import *
from excel_api import WriteDataToExcel
from excel_api import File
from tutorials import GameTutorial
import os
import time
from datetime import datetime


def get_datas(gametutorial_path, gametutorial_map, gametutorial_config_path):
    parse_tutorial = GameTutorial(gametutorial_path, gametutorial_map, gametutorial_config_path)
    mul_tutorial_files = parse_tutorial.get_tutorial_files()

    datas = {}
    adjust_tokes = []
    other_tutorial_values_multi = []
    for tutorial_name, tutorial_files in mul_tutorial_files.items():
        tutorials = parse_tutorial.get_tutorials(tutorial_name, tutorial_files)
        #解析正常数据
        title = list(tutorials[0].keys())
        values = [list(tutorial.values()) for tutorial in tutorials if tutorial.get('level') >= 0]
        values.insert(0, title)
        datas[tutorial_name] = values
        #解析不需要处理的数据
        for tutorial in tutorials:
            values = list(tutorial.values())
            adjust_values = [tutorial.get('step_name', ''), tutorial.get('adjust_token', '')]
            if tutorial.get('level') < 0 and values not in other_tutorial_values_multi:
                other_tutorial_values_multi.append(values)
            elif tutorial.get('level') >= 0 and adjust_values not in adjust_tokes:
                adjust_tokes.append(adjust_values)

    # sorted other_tutorial_values_multi
    other_tutorial_values_multi = sorted(other_tutorial_values_multi, key=lambda x: (x[0], x[2])) #sorted
    other_tutorial_values_multi.insert(0, title)
    datas['other_tutorial'] = other_tutorial_values_multi

    # sorted adjust_tokes
    adjust_tokes = sorted(adjust_tokes, key=lambda x: x[0])
    adjust_tokes.insert(0, ['step_name', 'adjust_token'])
    datas['adjust_tokes'] = adjust_tokes
    return datas

def write_data_to_excel(tutorial_output_path, datas):
    write_data_to_excel = WriteDataToExcel(tutorial_output_path)
    write_data_to_excel.write_sheets(datas)
    for sheetname in datas:
        if sheetname == 'adjust_tokes':
            write_data_to_excel.write_cell(sheetname, "C1", 'is_check')
            write_data_to_excel.set_sheet_formula_conditional(sheetname, 'A1:C10000', '=$C1=1', bg_color='#00b8ff')
        else:
            write_data_to_excel.set_sheet_formula_conditional(sheetname, 'A1:J10000', '=$D1="well_done"')
            write_data_to_excel.write_cell(sheetname, "K1", 'is_check')
            write_data_to_excel.set_sheet_formula_conditional(sheetname, 'A1:I10000', '=$K1=1', bg_color='#00b8ff')
    write_data_to_excel.close()


def game_write_main(gametutorial_path, gametutorial_map, gametutorial_config_path, gametutorial_output_path='./output'):
    filename = datetime.now().strftime('%Y%m%d')
    tutorial_output_path = os.path.join(gametutorial_output_path, f'{filename}gametutorial.xlsx')
    file = File(tutorial_output_path)
    file.close_file()
    time.sleep(2)
    datas = get_datas(gametutorial_path, gametutorial_map, gametutorial_config_path)
    write_data_to_excel(tutorial_output_path, datas)
    file.open_file()

if __name__ == '__main__':
    game_write_main(gametutorial_path, gametutorial_map, gametutorial_config_path)
