'''
@Author: longfengpili
@Date: 2019-12-12 11:03:01
@LastEditTime: 2019-12-12 15:11:41
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

    def get_datas_from_file(self):
        r_excel = ReadDataFromExcel(self.storytutorial_file)
        datas = r_excel.get_sheet_values_by_columns(self.sheetname, self.columns, header_row=2)
        datas = list(filter(lambda data: sum(map(lambda elem: isinstance(elem, str) if elem else 0, data)) == 0, datas)) #过滤掉有字符串的row
        datas = list(map(lambda data: list(map(lambda elem: int(elem) if elem else 0, data)), datas)) #全部转换成int
        datas = list(filter(lambda data: data[-1] > 0, datas)) # 过滤掉BI = 0 的数据
        return datas

    def combin_story_funnel(self, datas):
        funnel_datas = {}
        id = 0
        current_questid = None
        story_funnel = []
        story_funnel.append(['game_version', 'id', 'storyid', 'questid', 'bi', 'status'])
        for ix, data in enumerate(datas):
            data = data.copy()
            _, questid, bi = data
            if questid != 0 and questid != current_questid:
                if current_questid:
                    id += 1
                    story_funnel.append([self.game_version, id, current_questid, current_questid, datas[ix-1][-1], 'end']) #结束上一个
                current_questid = questid
                id += 1
                story_funnel.append([self.game_version, id, current_questid, current_questid, bi, 'start']) #开始下一个
            id += 1
            data = [self.game_version, id] + data + ['start']
            story_funnel.append(data)
        funnel_datas['story_funnel'] = story_funnel
        funnel_datas['quest_funnel'] = [step for ix, step in enumerate(story_funnel) if step[2] == step[3] or ix == 0]
        return funnel_datas








    
