# -*- encoding:utf-8 -*-

import engine
import asyncio

import engine

def setup_config(config_file):
	content = open(config_file).read()

	config = {}
	exec(content, config)

	engine._config = config

def setup_event_loop():
	engine._event_loop = asyncio.get_event_loop()

def init_server(config_file):
	setup_config(config_file)