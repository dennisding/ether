# -*- coding:utf-8 -*-

import asyncio
import engine

from . import client_mgr
from . import game_mgr

class EntityInfo:
	def __init__(self, eid, cid = 0, gameid = 0):
		self.eid = eid
		self.cid = cid
		self.gameid = gameid

class Gate:
	def __init__(self):
		engine._server = self

		self.gid = engine.config()['gid']

		self.entity_infos = {}  # {eid:infos}
		self.client_infos = {} # {cid : infos}

	def on_entity_created(self, eid, cid, gameid):
		infos = EntityInfo(eid, cid, gameid)
		assert eid not in self.entity_infos
		assert cid not in self.client_infos

		self.entity_infos[eid] = infos
		self.client_infos[cid] = infos

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
