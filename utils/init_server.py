# -*- encoding:utf-8 -*-

import sys
import engine
import asyncio
import pathlib

import engine

def setup_game_config():
	with open(engine.args().gconfig) as f:
		content = f.read()
		config = {}
		exec(content, config)
		engine._game_config = config

	path = pathlib.Path(engine.game_config()['entity_path'])
	sys.path.insert(0, str(path.resolve()))

def setup_config():
	args = engine.args()

	with open(args.config) as f:
		content = f.read()
		config = {}
		exec(content, config)

		# setup common
		result = dict(config[args.name])
		result['name'] = args.name

		def add_config(configs):
			for key, value in configs.items():
				if key not in result and key != '__builtins__':
					result[key] = value

		add_config(config.get('common', {}))
		add_config(config)

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