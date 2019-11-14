'''
@Author: longfengpili
@Date: 2019-11-14 18:24:59
@LastEditTime: 2019-11-14 18:31:02
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


from mysetting import *
from parse_tutorial import ParseTutorial

def test_parse():
    pt = ParseTutorial(project_tutorial_path, tutorial_map, tutorial_especial_path)
    tutorial_files = pt.get_tutorial_files()
    print(tutorial_files.keys())

def test_parse2():
    pt = ParseTutorial(project_tutorial_path, tutorial_map, tutorial_especial_path)
    tutorial_files = p.get_tutorial_files()
    print(tutorial_files.keys())