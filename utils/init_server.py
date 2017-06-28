# -*- encoding:utf-8 -*-

import engine
import asyncio

import engine

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

def init_server(args):
	# setup the args
	engine._args = args

	setup_config()