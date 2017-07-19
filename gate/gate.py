# -*- coding:utf-8 -*-

import asyncio
import engine

from . import client_mgr
from . import game_mgr

class Gate:
	def __init__(self):
		engine._server = self

		self.gid = engine.config()['gid']

		self.eid2cid = {}
		self.cid2eid = {}

	def setup_connection(self, eid, cid):
		self.eid2cid[eid] = cid
		self.cid2eid[cid] = eid

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

	def get_client(self, cid):
		return self.client_mgr.get_client(cid)

	def run_forever(self):
		loop = asyncio.get_event_loop()
		loop.run_forever()
