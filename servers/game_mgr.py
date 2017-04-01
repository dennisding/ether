# -*- encoding:utf-8 -*-

import engine

class GameMgr:
	def __init__(self):
		engine._server = self

	def start(self):
		self.prepare_server()

	def prepare_server(self):
		pass
