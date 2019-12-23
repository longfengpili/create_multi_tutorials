'''
@Author: longfengpili
@Date: 2019-12-12 11:03:01
@LastEditTime : 2019-12-23 13:13:49
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from excel_api import ReadDataFromExcel
from mysetting import *

class StoryTutorial(object):
    
    def __init__(self, storytutorial_file, game_version):
        self.storytutorial_file = storytutorial_file
        self.game_version = game_version
        self.sheetname = 'StoryDialogStep'
        self.columns = ['id', 'Questid', 'BI']
        self.id = 0

    def get_datas_from_file(self):
        r_excel = ReadDataFromExcel(self.storytutorial_file)
        datas = r_excel.get_sheet_values_by_columns(self.sheetname, self.columns, header_row=2)
        datas = list(map(lambda data: list(map(lambda elem: -1 if elem == 'gift' else elem, data)), datas)) #gift转换成-1
        datas = list(filter(lambda data: sum(map(lambda elem: isinstance(elem, str) if elem else 0, data)) == 0, datas)) #过滤掉有字符串的row
        datas = list(map(lambda data: list(map(lambda elem: int(elem) if elem else 0, data)), datas)) #全部转换成int
        datas = list(filter(lambda data: data[-1] > 0, datas)) # 过滤掉BI = 0 的数据
        return datas

    def combin_story_id_single(self, storyid, questid, bi, state):
        self.id += 1
        story_single = [self.id, self.game_version, storyid, questid, bi, state]
        return story_single

    def combin_story_id_single_two(self, storyid, questid, bi):
        story_single_two = []
        story_single = self.combin_story_id_single(storyid, questid, bi, 'start')
        story_single_two.append(story_single)
        story_single = self.combin_story_id_single(storyid, questid, bi, 'end')
        story_single_two.append(story_single)
        return story_single_two

    def combin_story_funnel(self, datas):
        funnel_datas = {}
        id = 0
        current_questid = None
        story_funnel = []
        story_funnel.append(['id', 'game_version', 'storyid', 'questid', 'bi', 'state'])
        for ix, data in enumerate(datas):
            data = data.copy()
            dialogid, questid, bi = data
            questid = 'gift' if questid == -1 else '' if questid == 0 else questid

            # 新任务，结束任务
            if current_questid != questid and current_questid and current_questid != 'gift':
                story_single = self.combin_story_id_single(current_questid, current_questid, bi, 'end') # 结束任务
                story_funnel.append(story_single)
            # 新任务，开始任务
            if dialogid == 0 or (current_questid != questid and questid and questid != 'gift'):
                current_questid = questid
                story_single = self.combin_story_id_single(current_questid, current_questid, bi, 'start') # 开始任务
                story_funnel.append(story_single)
            # 存在dialog
            if dialogid != 0:
                current_questid = questid
                story_single_two = self.combin_story_id_single_two(dialogid, current_questid, bi)
                story_funnel.extend(story_single_two)
            # 最后一次
            if ix + 1 == len(datas):
                story_single = self.combin_story_id_single(current_questid, current_questid, bi, 'end') # 结束任务
                story_funnel.append(story_single)
            
        funnel_datas['story_funnel'] = story_funnel
        # funnel_datas['quest_funnel'] = [step for ix, step in enumerate(story_funnel) if step[2] == step[3] or ix == 0]
        return funnel_datas








    
