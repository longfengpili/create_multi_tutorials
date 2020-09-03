'''
@Author: longfengpili
@Date: 2019-11-13 16:04:28
@LastEditTime : 2019-12-23 12:20:06
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from mysetting import *
from excel_api import WriteDataToExcel
from excel_api import File
from tutorials import QuestTutorial
import os
import time
from datetime import datetime



def quest_tutorial_main(quest_file, game_version, q_start, q_end):
    qt = QuestTutorial(quest_file, game_version)
    quests_d, quests_l = qt.get_quests_from_file()
    longpath = qt.find_long_questpath(quests_d, start=q_end, end=q_start)
    print(longpath)
    qt.save_questpath(quests_l)

if __name__ == '__main__':
    quest_tutorial_main(quest_file, game_version, q_start, q_end)
