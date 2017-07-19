# -*- coding:utf-8 -*-

import sys
import pathlib
import asyncio
import engine

from . import entity
from . import gate_mgr
from . import game_mgr

from utils import entity_mgr

class Game:
	def __init__(self):
		engine._server = self

	def serve(self):
		self.prepare_environment()
		self.run_init_function()
		self.setup_entity_mgr()

		self.gate_mgr = gate_mgr.GateMgr()
		self.game_mgr = game_mgr.GameMgr()

		self.gate_mgr.connect_gates()
		self.game_mgr.connect_games()

		self.run_forever()

	def prepare_environment(self):
		path = pathlib.Path(engine.game_config()['entity_path'])
		sys.path.insert(0, str(path.resolve()))

	def run_init_function(self):
		tokens = engine.game_config()['init_fun'].split('.')
		module_name = '.'.join(tokens[:-1])
		fun_name = tokens[-1]

		__import__(module_name)
		module = sys.modules[module_name]

		fun = getattr(module, fun_name, None)
		fun and fun()

	def get_gate(self, gid):
		return self.gate_mgr.get_gate(gid)

	def get_game(self, gid):
		return self.game_mgr.get_game(gid)

	def setup_entity_mgr(self):
		self.entity_mgr = entity_mgr.EntityMgr()

		game_config = engine.game_config()
		def_path = game_config['entity_def_path']
		entity_path = game_config['entity_path']

		self.entity_mgr.prepare_entities(def_path, entity_path, entity.LocalEntity)

	def run_forever(self):
		loop = asyncio.get_event_loop()
		loop.run_forever()
