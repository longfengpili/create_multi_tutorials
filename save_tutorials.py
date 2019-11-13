'''
@Author: longfengpili
@Date: 2019-11-13 16:04:28
@LastEditTime: 2019-11-13 16:47:29
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from mysetting import *
from to_excel import WriteDataToExcel
from parse_tutorial import ParseTutorial


parse_tutorial = ParseTutorial(project_tutorial_path, tutorial_map, tutorial_especial_path)
mul_tutorial_files = parse_tutorial.get_tutorial_files()

datas = {}
adjust_keys = set()
for tutorial_name, tutorial_files in mul_tutorial_files.items():
    tutorials = parse_tutorial.get_tutorials(tutorial_name, tutorial_files)
    title = list(tutorials[0].keys())
    adjust_key = set([tutorial.get('step_name') for tutorial in tutorials if tutorial.get('level') >= 0])
    adjust_keys.update(adjust_key)
    values = [tutorial.values() for tutorial in tutorials]
    values.insert(0, title)
    datas[tutorial_name] = values


write_data_to_excel = WriteDataToExcel(tutorial_output_path)
write_data_to_excel.write_sheets(datas)
for sheetname in datas:
    write_data_to_excel.set_sheet_formula_conditional(sheetname, 'A1:I10000', '=$E1="well_done"')
write_data_to_excel.close()