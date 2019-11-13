'''
@Author: longfengpili
@Date: 2019-11-13 16:04:28
@LastEditTime: 2019-11-13 17:56:12
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
other_tutorial_values_multi = []
for tutorial_name, tutorial_files in mul_tutorial_files.items():
    tutorials = parse_tutorial.get_tutorials(tutorial_name, tutorial_files)
    #解析正常数据
    title = list(tutorials[0].keys())
    values = [list(tutorial.values()) for tutorial in tutorials if tutorial.get('level') >= 0]
    values.insert(0, title)
    datas[tutorial_name] = values
    #解析不需要处理的数据
    other_tutorial_values = [list(tutorial.values()) for tutorial in tutorials if tutorial.get('level') < 0]
    other_tutorial_values_multi.extend(other_tutorial_values)
    #解析adjust数据
    adjust_key = set([tutorial.get('step_name') for tutorial in tutorials if tutorial.get('level') >= 0])
    adjust_keys.update(adjust_key)

other_tutorial_values_multi = sorted(other_tutorial_values_multi, key=lambda x: (x[0], x[2]))
# print(other_tutorial_values_multi)
other_tutorial_values_multi.insert(0, title)
datas['other_tutorial'] = other_tutorial_values_multi
datas['adjust_key'] = list(zip(sorted(adjust_keys)))


write_data_to_excel = WriteDataToExcel(tutorial_output_path)
write_data_to_excel.write_sheets(datas)
for sheetname in datas:
    write_data_to_excel.set_sheet_formula_conditional(sheetname, 'A1:I10000', '=$D1="well_done"')
write_data_to_excel.close()
