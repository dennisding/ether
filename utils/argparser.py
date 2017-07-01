# -*- coding:utf-8 -*-

import argparse

def parse_args():
	# python start.py gate gate1
	parser = argparse.ArgumentParser(description = 'Start the Gate, Game or DbMgr')

	parser.add_argument('type', type = str, choices=['client', 'gate', 'game', 'dbmgr'])
	parser.add_argument('name', type = str)
	parser.add_argument('--config', type = str, default = 'engine_config.py')
	parser.add_argument('--gconfig', type = str, default = 'game_config.py')

	return parser.parse_args()

