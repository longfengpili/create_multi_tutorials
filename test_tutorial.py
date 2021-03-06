'''
@Author: longfengpili
@Date: 2019-11-14 18:24:59
@LastEditTime : 2020-01-10 12:10:42
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


from mysetting import *
from tutorials import GameTutorial, StoryTutorial
import pytest
from excel_api import File
import time


def test_gametutorial():
    pt = GameTutorial(gametutorial_path, gametutorial_map, gametutorial_config_path, game_version='test')
    tutorial_files = pt.get_tutorial_files()
    print(tutorial_files)


def test_parse2():
    pt = GameTutorial(gametutorial_path, gametutorial_map, gametutorial_config_path, game_version='test')
    tutorial_levels = pt.get_tutorial_level_info(tutorial_name='【0】对照组(202001)')
    print(tutorial_levels)

@pytest.mark.skip()
def test_file_function():
    file = File('./output/tutorials.xlsx')
    # file.open_file()
    # time.sleep(10)
    # file.close_file()
    # file.del_file()

@pytest.mark.skip()
def test_story_tutorial():
    s_tutorial = StoryTutorial(storytutorial_file, game_version='test')
    datas = s_tutorial.get_datas_from_file()
    s = s_tutorial.combin_story_funnel(datas)
    print(s)
