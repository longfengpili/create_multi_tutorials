'''
@Author: longfengpili
@Date: 2019-11-14 18:24:59
@LastEditTime: 2019-12-12 12:25:48
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


from mysetting import *
from tutorials import GameTutorial, StoryTutorial
import pytest
from excel_api import File
import time

@pytest.mark.skip()
def test_parse():
    pt = GameTutorial(gametutorial_path, gametutorial_map, gametutorial_config_path)
    tutorial_files = pt.get_tutorial_adjust_id()
    print(tutorial_files)

@pytest.mark.skip()
def test_parse2():
    pt = GameTutorial(gametutorial_path, gametutorial_map, gametutorial_config_path)
    tutorial_files = pt.get_tutorial_files()
    print(tutorial_files)

@pytest.mark.skip()
def test_file_function():
    file = File('./output/tutorials.xlsx')
    # file.open_file()
    # time.sleep(10)
    # file.close_file()
    # file.del_file()

def test_story_tutorial():
    s_tutorial = StoryTutorial(storytutorial_file)
    datas = s_tutorial.get_datas_from_file()
    s = s_tutorial.combin_story_funnel(datas)
    print(s)
