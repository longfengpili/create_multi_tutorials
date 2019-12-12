'''
@Author: longfengpili
@Date: 2019-12-12 15:33:09
@LastEditTime: 2019-12-12 15:34:42
@github: https://github.com/longfengpili
'''
#!/usr/bin/env python3
#-*- coding:utf-8 -*-


from game_tutorials_main import game_write_main
from story_tutorials_main import story_write_main
from mysetting import *


game_write_main(gametutorial_path, gametutorial_map, gametutorial_config_path, game_version)
story_write_main(storytutorial_file, game_version)
