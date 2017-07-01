# -*- coding:utf-8 -*-

import asyncio
import engine

from . import client_mgr
from . import game_mgr

class Gate:
	def __init__(self):
		engine._server = self

		self.gid = engine.config()['gid']

	def serve(self):
		self.start_client_service()
		self.start_game_service()

		self.run_forever()

	def start_client_service(self):
		self.client_mgr = client_mgr.ClientMgr()

		self.client_mgr.serve()

	def start_game_service(self):
		self.game_mgr = game_mgr.GameMgr()
		self.game_mgr.serve()

	def run_forever(self):
		loop = asyncio.get_event_loop()
		loop.run_forever()
