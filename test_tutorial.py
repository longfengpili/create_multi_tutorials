'''
@Author: longfengpili
@Date: 2019-11-14 18:24:59
@LastEditTime: 2019-11-15 14:28:17
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


from mysetting import *
from parse_tutorial import ParseTutorial
import pytest
from windows import File
import time

# @pytest.mark.skip()
def test_parse():
    pt = ParseTutorial(project_tutorial_path, tutorial_map, tutorial_config_path)
    tutorial_files = pt.get_tutorial_adjust_id()
    print(tutorial_files)

# @pytest.mark.skip()
def test_parse2():
    pt = ParseTutorial(project_tutorial_path, tutorial_map, tutorial_config_path)
    tutorial_files = p.get_tutorial_files()
    print(tutorial_files)

def test_file_function():
    file = File('./output/tutorials.xlsx')
    print(file.file_path())
    # file.open_file()
    # time.sleep(10)
    # file.close_file()
    # file.del_file()
