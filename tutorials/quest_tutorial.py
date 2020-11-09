'''
@Author: longfengpili
@Date: 2019-12-12 11:03:01
@LastEditTime : 2019-12-23 13:13:49
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from datetime import datetime
from graphviz import Digraph

from excel_api import ReadDataFromExcel
from mysetting import *

class QuestTutorial(object):
    
    def __init__(self, quest_file, game_version):
        self.quest_file = quest_file
        self.game_version = game_version
        self.sheetname = 'Quest_AB0'
        self.columns = ['id', 'PreQuestIds']

    def get_quests_from_file(self):
        quests_d = {}
        quests_l = []
        r_excel = ReadDataFromExcel(self.quest_file)
        datas = r_excel.get_sheet_values_by_columns(self.sheetname, self.columns, header_row=2)
        datas = datas[2:]
        datas = [[q if isinstance(q, str) else f"{q:.0f}" for q in data] for data in datas]
        for data in datas:
            quests_d[data[0]] =  data[1].split('#') if '#' in data[1] else [data[1]]
            if '#' in data[1]:
                for q in data[1].split('#'):
                    quests_l.append([q, data[0]])
            else:
                quests_l.append([data[1], data[0]])
        return quests_d, quests_l

    def find_long_questpath(self, quests_d, start, end, path=[]):
        path = path +[start]
        if start == end:
            return path
        
        long_path = []
        for node in quests_d.get(start):
            if node not in path:
                newpath = self.find_long_questpath(quests_d, node, end, path)
                if newpath:
                    if not long_path or len(newpath) > len(long_path):
                        long_path = newpath
        return long_path

    def save_questpath(self, quests_l):
        today = datetime.now().strftime('%Y%m%d')
        filename = today + 'questtutorial'
        dot = Digraph(name=filename, format='pdf', directory='./output')
        nodes = []
        for qs in quests_l:
            for q in qs:
                if q not in nodes:
                    dot.node(q)
                    nodes.append(q)
                dot.edge(qs[0], qs[1])
        dot.attr(rankdir='LR')
        dot.render()








    
