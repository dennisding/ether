# -*- encoding:utf-8 -*-

import sys
import engine
import asyncio

import engine

def setup_game_config():
	with open(engine.args().gconfig) as f:
		content = f.read()
		config = {}
		exec(content, config)
		engine._game_config = config

def setup_common_config(configs):
	common = configs.get('common', {})

	for key, config in configs.items():
		if not isinstance(config, dict) or key == 'common':
			continue

		for ckey, cvalue in common.items():
			if ckey not in config:
				config[ckey] = cvalue

def setup_config():
	args = engine.args()

	with open(args.config) as f:
		content = f.read()
		config = {}
		exec(content, config)

		setup_common_config(config)

		# setup common
		result = dict(config[args.name])
		result['name'] = args.name

		for key, value in config.items():
			if key not in result and key != '__builtins__':
				result[key] = value

		engine._config = result

def setup_win():
	loop = asyncio.ProactorEventLoop()
	asyncio.set_event_loop(loop)

def init_server(args):
	# setup the args
	engine._args = args

	setup_config()
	setup_game_config()

	if sys.platform == 'win32':
		setup_win()