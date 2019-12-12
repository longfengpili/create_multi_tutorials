'''
@Author: longfengpili
@Date: 2019-11-13 11:35:31
@LastEditTime: 2019-12-12 15:11:28
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from mysetting import *
import os
from bs4 import BeautifulSoup
import xlrd
import re
from excel_api import WriteDataToExcel

class GameTutorial(object):
    '''[summary]
    
    [description]
        1. level_step 设定，为了排序
            + enter_level 1.0
            + 关前道具 1.1
            + start_level 1.2
            + 关内引导 1.3
            + level_completed 1.4
            + well_done 1.5
            + 关后剧情 
        2. especial文档
            + level_tutorials 只是为了获取关前道具关卡
            + story_tutorials 是需要加入的其他关卡外漏斗（具体序号需要符合第一部分）
    Variables:
        tutorial_path {str} -- 文件地址
        tutorial_map {dict} -- 文件分类与especial中对应的列名
        tutorial_config_path ｛str｝-- tutorial_config_path文件地址
    '''
    
    def __init__(self, tutorial_path, tutorial_map, tutorial_config_path, game_version):
        self.tutorial_path = tutorial_path
        self.tutorial_map = tutorial_map
        self.tutorial_config_path = tutorial_config_path
        self.game_version = game_version

    def get_tutorial_files(self):
        '''
        @description: 获取tutorial文件并分组
        '''
        mul_tutorial_files = {}
        non_level_files = [] #公共部分

        all_files = os.listdir(self.tutorial_path)
        for xml, tutorial_name in self.tutorial_map.items():
            tutorial_levels = self.get_tutorial_level_info(tutorial_name)
            tutorial_levels = dict([(k, v) for k, v in tutorial_levels.items() if not isinstance(v, str)])
            for elem, level in tutorial_levels.items():
                if xml == 'AB0.xml':
                    file = [file for file in all_files if file.endswith('.xml') and re.search(f'level{int(level)}(?!\d)', file) and 'AB' not in file]
                else:
                    file1 = [file for file in all_files if file.endswith('.xml') and re.search(f'level{int(level)}(?!\d)', file) and xml in file]
                    file2 = [file for file in all_files if file.endswith('.xml') and re.search(f'level{int(level)}(?!\d)', file)]
                    file = file1 if file1 else file2
                if file:
                    file = file[0]
                    mul_tutorial_files.setdefault(tutorial_name, [])
                    mul_tutorial_files.get(tutorial_name).append(file)
                print(xml, elem, level, file)
        for file in all_files:
            if '.meta' not in file and '_a' not in file and '_R1' not in file:
                if 'level' not in file:
                    non_level_files.append(file)

        for tutorial_name in mul_tutorial_files:
            mul_tutorial_files.get(tutorial_name).extend(non_level_files)
        # print(mul_tutorial_files)
        # sys.exit(0)
        return mul_tutorial_files

    def get_tutorial_level_info(self, tutorial_name):
        '''
        @description: 根据tutorial_name获取especial中的内容
        @param {type} 
        【tutorial_name {str}】：对应ab组的name
        @return: 
        【tutorial_levels {dict}】：返回对应的各项道具、各种非关卡内引导的数据
        '''
        tutorial_names = [tutorial_name, 'all'] # 'all'是公共部分的对应数据
        with xlrd.open_workbook(self.tutorial_config_path) as wb:
            sheets_name = wb.sheet_names()
        sheets_name = [sheet_name for sheet_name in sheets_name if not sheet_name.startswith('_')]
        tutorial_levels = {}
        tutorial_levels_temp = {}
        for sheet_name in sheets_name:
            sheet = wb.sheet_by_name(sheet_name)
            col_level = sheet.col_values(0) #获取level列
            sheet_columns = sheet.row_values(0) #获取表头
            for tutorial_name in tutorial_names:
                if tutorial_name in sheet_columns:
                    col_values = sheet.col_values(sheet_columns.index(tutorial_name)) #获取对应的列的数据
                    elem_counts = [col_values.count(elem) for elem in set(col_values) if elem]
                    if max(elem_counts) >= 2: #检查是否有重复的
                        elems = [elem for elem in set(col_values) if col_values.count(elem) >= 2]
                        raise ValueError(f"mutiple elem {','.join(elems)}")
                    else:
                        temp = dict(zip(col_values[1:], col_level[1:]))
                        tutorial_levels_temp.update(temp)
        tutorial_levels_temp.pop('')
        
        for k, v in tutorial_levels_temp.items(): #key中的大写全部转成小写
            k = k.lower() if isinstance(k, str) else f'{int(k)}' if isinstance(k, int) or isinstance(k, float) else k
            tutorial_levels[k] = v
        return tutorial_levels

    def get_tutorial_adjust_token(self, adjust_sheet='adjust_funnel'):
        tutorial_adjust_id = {}
        with xlrd.open_workbook(self.tutorial_config_path) as wb:
            tutorial_adjust_sheet = wb.sheet_by_name(adjust_sheet)
        for row in range(tutorial_adjust_sheet.nrows):
            values = tutorial_adjust_sheet.row_values(row)
            if values and values[0] == 'new_user_funnel':
                key_ = values[1]
                key_ = key_.lower() if isinstance(key_, str) else f'{int(key_)}' if isinstance(key_, int) or isinstance(key_, float) else key_
                value_ = values[2]
                tutorial_adjust_id[key_] = value_
        return tutorial_adjust_id

    def get_tutorial_info_single(self, tutorial_file, tutorial_levels):
        '''
        @description: 获取单个文件的漏斗信息
        @param {type} 
        【tutorial_file {str}】：文件路径
        【tutorial_levels {dict}】：特别配置的信息
        @return: 
        【level {int}】：关卡号
        【file_tutorial {list}】：多步漏斗数据，每步是一个字典
        '''
        file_tutorial = []
        tutorial_file_path = os.path.join(self.tutorial_path, tutorial_file)
        with open(tutorial_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
            soup = BeautifulSoup(html, 'lxml')
            if soup.pbtutorial:
                id = soup.pbtutorial.get('id')
                result = re.search('(?<=level)(\d+)', id)
                level = float(result.group()) if result else None
            for soup_ in soup.find_all('steps'):
                tutorial = {}
                tutorial['tutorial_file'] = tutorial_file
                tutorial['game_version'] = self.game_version
                tutorial['level_group'] = id
                tutorial['step'] = int(soup_.get('move', 0))
                tutorial['step_name_ori'] = soup_.get('step_name', '')
                tutorial['step_des'] = soup_.get('step_des', '')
                # tutorial['adjust_token'] = None  # 占位
                tutorial['step_name'] = tutorial['step_name_ori'] + '_s'
                tutorial['level'] = None #占位

                if level:
                    tutorial['level_step'] = level + 0.3
                elif 'selectBooster' in tutorial_file: #关前道具没有配置关卡号
                    t_ = tutorial['step_name_ori'].split('_learning')[0]
                    level = tutorial_levels.get(t_.lower(), 0) + 0.1
                    tutorial['level_step'] = level
                else:
                    # print(f"【{tutorial_file}({level})】{tutorial['step_name']}")
                    tutorial['level_step'] = -10000
                tutorial['level'] = int(tutorial['level_step'])

                if soup_.dialog:
                    tutorial['step_text'] = soup_.dialog.get('text', '')
                else:
                    tutorial['step_text'] = ''
                file_tutorial.append(tutorial)

        end = file_tutorial[-1].copy()
        if end.get('step_name'):
            if end.get('step_name')[-2:] == '_s':
                end['step'] += 1
                end['step_name'] = end.get('step_name').replace('_s', '_e')
                end['step_des'] = end['step_des'] + '结束_temp'
                file_tutorial.append(end)
        return tutorial['level'], file_tutorial

    def get_tutorial_info_multiple(self, tutorial_files, tutorial_levels):
        levels = []
        inlevel_tutorials = []
        for tutorial_file in tutorial_files:
            level, file_tutorial = self.get_tutorial_info_single(tutorial_file, tutorial_levels)
            levels.append(level)
            inlevel_tutorials.extend(file_tutorial)
    
        return levels, inlevel_tutorials
    
    def get_story_tutorial_info(self, tutorial_levels):
        '''
        @description: 生成关卡外剧情的漏斗数据
        @param {type} 
        @return: 
        '''
        story_tutorials = []
        for k, v in tutorial_levels.items():
            if isinstance(v, str):
                level, step = v.split('-', 1)
                tutorial = {}
                tutorial['tutorial_file'] = ''
                tutorial['game_version'] = self.game_version
                tutorial['level_group'] = ''
                tutorial['step'] = int(step)
                tutorial['step_name_ori'] = k.split('.')[0]
                tutorial['step_des'] = ''
                # tutorial['adjust_token'] = None  # 占位
                tutorial['step_name'] = k.split('.')[0]
                tutorial['level'] = None #占位
                tutorial['level_step'] = float(level)
                tutorial['level'] = int(tutorial['level_step'])
                tutorial['step_text'] = ''
                story_tutorials.append(tutorial)
        return story_tutorials

    def get_levelstep_tutorial_info(self, levels, max_level=100):
        levels = set(list(range(max_level+1)) + levels)
        levels = [level for level in levels if level > 0]
        level_steps = {'enter_level': 0.0, 'start_level': 0.2,
                    'level_completed': 0.4, 'well_done': 0.5}
        levelstep_tutorials = []
        for lv in levels:
            for step in level_steps:
                tutorial = {}
                tutorial['tutorial_file'] = ''
                tutorial['game_version'] = self.game_version
                tutorial['level_group'] = ''
                tutorial['step'] = 0
                tutorial['step_name_ori'] = step
                tutorial['step_des'] = ''
                # tutorial['adjust_token'] = None  # 占位
                tutorial['step_name'] = step
                tutorial['level'] = None #占位
                tutorial['level_step'] = lv + level_steps[step]
                tutorial['level'] = int(tutorial['level_step'])
                tutorial['step_text'] = ''
                levelstep_tutorials.append(tutorial)

        return levelstep_tutorials

    def get_tutorials(self, tutorial_name, tutorial_files):
        tutorials_t = []
        tutorials = []
        tutorial_levels = self.get_tutorial_level_info(tutorial_name)
        levels, inlevel_tutorials = self.get_tutorial_info_multiple(tutorial_files, tutorial_levels)
        story_tutorials = self.get_story_tutorial_info(tutorial_levels)
        levelstep_tutorials = self.get_levelstep_tutorial_info(levels)
        tutorials_t.extend(inlevel_tutorials)
        tutorials_t.extend(story_tutorials)
        tutorials_t.extend(levelstep_tutorials)
        
        tutorials_token = self.get_tutorial_adjust_token(adjust_sheet='adjust_funnel')
        for tutorial in tutorials_t:
            step_name = tutorial.get('step_name', '')
            step_token = tutorials_token.get(step_name, '')
            tutorial['adjust_token'] = step_token
            tutorials.append(tutorial)

        tutorials = sorted(tutorials, key=lambda x: (x.get('level_step'), x.get('step')))
        return tutorials






