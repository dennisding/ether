# -*- coding:utf-8 -*-

import asyncio
import engine

from . import gate_mgr
from . import game_mgr
from . import entity_mgr

class Game:
	def __init__(self):
		engine._server = self

	def serve(self):
		self.setup_entity_mgr()

		self.gate_mgr = gate_mgr.GateMgr()
		self.game_mgr = game_mgr.GameMgr()

		self.gate_mgr.connect_gates()
		self.game_mgr.connect_games()

		self.run_forever()

	def setup_entity_mgr(self):
		self.entity_mgr = entity_mgr.EntityMgr()
		self.entity_mgr.load_entities(engine.game_config()['entity_path'])

	def run_forever(self):
		loop = asyncio.get_event_loop()
		loop.run_forever()
